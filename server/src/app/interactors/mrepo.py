from distutils.log import error
from app.domain.mrepo import AddParsedResultInput, MonitoredRepo

from infra.storage.mrepodb import read_monitored_repo, create_parse_report
from infra.storage.userdb import read_user
from infra.integration.github import get_github_repo_last_commit

from typing import Union, TypedDict
from typing_extensions import Literal


class WriteParseResultOutput(TypedDict):
    status: Literal["success", "failed"]
    error: Union[str, None]


class MonitoredRepoInteractor:
    def __init__(self) -> None:
        # infra.storage.mrepodb
        # infra.storage.userdb
        # infra.integration.github
        pass

    async def execute_write_parse_result(
        self, payload: AddParsedResultInput
    ) -> WriteParseResultOutput:
        try:
            output: WriteParseResultOutput

            mrepo: MonitoredRepo = await read_monitored_repo(payload["mrepoId"])

            if mrepo is None:
                output = dict(
                    status="failed",
                    error="Requested repository is not monitored, add the repo first",
                )
                return output

            if (mrepo is not None) and (mrepo.status == "inactive"):
                output = dict(status="failed", error="Requested repository is inactive")
                return output

            user = await read_user(mrepo.userId)

            """
              The hash of the latest commit is required to create parse report.
            """
            oauth_token = user.oauth[0]["token"]

            gh_call_output = await get_github_repo_last_commit(
                oauth_token, mrepo.fullName, mrepo.defaultBranch
            )

            if gh_call_output["status"] == "failed":
                output = dict(status="failed", error=gh_call_output["error"])

            if gh_call_output["status"] == "success":
                commit_hash = gh_call_output["commit"]
                await create_parse_report(commit_hash, payload)
                output = dict(status="success")

            return output
        except Exception as e:
            raise e
