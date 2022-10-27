from app.domain.mrepo import AddMonitoredReposInput, AddParsedResultInput, MonitoredRepo

from infra.storage.mrepodb import MonitoredRepoDBAccess
from infra.storage.userdb import UserDBAccess
from infra.integration.github import GitHubService

from uuid import UUID
from typing import Union, TypedDict, List
from typing_extensions import Literal


class MonitoredRepoBaseUseCase:
    def __init__(
        self,
        userdb: UserDBAccess,
        mrepodb: MonitoredRepoDBAccess,
        github: GitHubService,
    ) -> None:
        self.userdb = userdb
        self.mrepodb = mrepodb
        self.github = github


class GetMonitoredRepoUseCase(MonitoredRepoBaseUseCase):
    async def execute(self, email: str, mrepo_id: UUID) -> MonitoredRepo:
        try:
            user = await self.userdb.read_user_by_email(email)

            if user is None:
                raise ValueError("unknown user")

            mrepo = await self.mrepodb.read_monitored_repo(mrepo_id)

            if mrepo is None:
                raise ValueError("unknown monitored repositry")

            return mrepo
        except ValueError as e:
            raise e
        except Exception as e:
            raise e


class GetMonitoredReposUseCase(MonitoredRepoBaseUseCase):
    async def execute(self, email: str, limit: int, offset: int) -> List[MonitoredRepo]:
        try:
            user = await self.userdb.read_user_by_email(email)

            if user is None:
                raise ValueError("unknown user")

            mrepos = await self.mrepodb.read_monitored_repos(
                user.id, "active", limit, offset
            )

            return mrepos
        except Exception as e:
            raise e


class AddMonitoredReposUseCase(MonitoredRepoBaseUseCase):
    async def execute(
        self, email: str, payload: AddMonitoredReposInput
    ) -> List[MonitoredRepo]:
        try:
            user = await self.userdb.read_user_by_email(email)
            user_id = user.id

            new_monitroed_repos: List[MonitoredRepo] = []
            oauth_token = user.oauth[0]["token"]

            if len(payload["repos"]) > 0:
                for repo in payload["repos"]:

                    repo = dict(repo)
                    github_repo_check = await self.github.get_github_repo(
                        oauth_token, repo["fullName"]
                    )

                    if github_repo_check["status"] == "fail":
                        self.logger.warning(
                            f"Non-existing GitHub repository was requested for monitoring | user_id: {user_id} | repo_fullname: {repo['fullName']}"
                        )

                    if github_repo_check["status"] == "success":
                        duplication_check_result = (
                            await self.mrepodb.read_monitored_repo_by_fullname(
                                repo["fullName"], "github"
                            )
                        )

                        if duplication_check_result is None:
                            """Adding a new repository"""
                            new_repo = await self.mrepodb.create_monitored_repo(
                                repo, user_id
                            )
                            new_monitroed_repos.append(new_repo)
                            await self.github.register_push_github_repo(
                                oauth_token, repo["fullName"]
                            )
                        else:
                            """Skipping as it's already monitored repository"""
                            self.logger.warning(
                                f"Already monitored repository was included in the | user_id: {user_id} | repo_name: {repo['fullName']}"
                            )

            return new_monitroed_repos

        except Exception as e:
            raise e


class WriteParseResultOutput(TypedDict):
    status: Literal["success", "failed"]
    error: Union[str, None]


class WriteParseResultUseCase(MonitoredRepoBaseUseCase):
    async def execute(self, payload: AddParsedResultInput) -> WriteParseResultOutput:
        try:
            output: WriteParseResultOutput

            mrepo: MonitoredRepo = await self.mrepodb.read_monitored_repo(
                payload["mrepoId"]
            )

            if mrepo is None:
                output = dict(
                    status="failed",
                    error="Requested repository is not monitored, add the repo first",
                )
                return output

            if (mrepo is not None) and (mrepo.status == "inactive"):
                output = dict(status="failed", error="Requested repository is inactive")
                return output

            user = await self.userdb.read_user(mrepo.userId)

            """
              The hash of the latest commit is required to create parse report.
            """
            oauth_token = user.oauth[0]["token"]

            gh_call_output = await self.github.get_github_repo_last_commit(
                oauth_token, mrepo.fullName, mrepo.defaultBranch
            )

            if gh_call_output["status"] == "failed":
                output = dict(status="failed", error=gh_call_output["error"])

            if gh_call_output["status"] == "success":
                await self.mrepodb.create_parse_report(
                    gh_call_output["commit"], payload
                )
                output = dict(status="success")

            return output
        except Exception as e:
            raise e


class MonitoredRepoInteractor:
    def __init__(
        self,
        get_mrepo: GetMonitoredRepoUseCase,
        get_mrepos: GetMonitoredReposUseCase,
        add_mrepos: AddMonitoredReposUseCase,
        write_parse_result: WriteParseResultUseCase,
    ) -> None:
        self.get_mrepo = get_mrepo
        self.get_mrepos = get_mrepos
        self.add_mrepos = add_mrepos
        self.write_parse_result = write_parse_result
