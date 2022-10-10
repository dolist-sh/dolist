from app.domain.user import User
from app.domain.mrepo import AddMonitoredReposInput, MonitoredRepo

from infra.storage.userdb import UserDBAccess
from infra.integration.github import GitHubService, GetGitHubRepoOutput
from infra.storage.mrepodb import MonitoredRepoDBAccess

from logging import Logger
from typing import List


class UserInteractor:
    def __init__(
        self,
        userdb: UserDBAccess,
        mrepodb: MonitoredRepoDBAccess,
        github: GitHubService,
        logger: Logger,
    ) -> None:
        self.userdb = userdb
        self.mrepodb = mrepodb
        self.github = github
        self.logger = logger

    async def execute_get_user(self, email: str) -> User:
        try:
            user = await self.userdb.read_user_by_email(email)

            if user is None:
                raise ValueError("User not found")
            else:
                return user
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    async def execute_get_user_github_repos(self, email: str):
        try:
            user = await self.userdb.read_user_by_email(email)
            github_token = user.oauth[0]["token"]  # TODO: Replace this with find call

            output: GetGitHubRepoOutput = await self.github.get_github_repo_list(
                github_token
            )

            if output["status"] == "success":
                return output["data"]
            else:
                raise ValueError(output["error"])
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    async def execute_add_monitored_repos(
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
