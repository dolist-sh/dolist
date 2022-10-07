from app.domain.mrepo import AddParsedResultInput, MonitoredRepo

from infra.storage.mrepodb import MonitoredRepoDBAdaptor
from infra.storage.userdb import UserDBAdaptor
from infra.integration.github import GitHubAdaptor

from typing import Union, TypedDict
from typing_extensions import Literal


class WriteParseResultOutput(TypedDict):
    status: Literal["success", "failed"]
    error: Union[str, None]


class MonitoredRepoInteractor:
    def __init__(
        self,
        userdb: UserDBAdaptor,
        mrepodb: MonitoredRepoDBAdaptor,
        github: GitHubAdaptor,
    ) -> None:
        self.userdb = userdb
        self.mrepodb = mrepodb
        self.github = github

    async def execute_write_parse_result(
        self, payload: AddParsedResultInput
    ) -> WriteParseResultOutput:
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
