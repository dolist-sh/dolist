import requests
from logging import Logger

from typing import Union, List
from typing_extensions import Literal, TypedDict


class GitHubCallOutput(TypedDict):
    status: Literal["success", "failed"]
    error: Union[str, None]


class GetGitHubRepoOutput(GitHubCallOutput):
    data: str  # JSON object


class GetGitHubRepoListOutput(GitHubCallOutput):
    data: List[str]  # List of JSON


class GetGitHubRepoLastCommitOutput(GitHubCallOutput):
    commit: str


class GitHubAdaptor:
    def __init__(self, requests: requests, logger: Logger) -> None:
        self.requests = requests
        self.logger = logger

    async def get_github_repo(self, access_token: str, full_name: str):
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {access_token}",
            }
            host = f"https://api.github.com/repos/{full_name}"

            res = self.requests.get(host, headers=headers)

            output: GetGitHubRepoOutput

            if res.status_code == 200:
                self.logger.info(
                    f"Requested GitHub repositories for authenticated user successfully returned from GitHub API"
                )
                output = dict(status="success", data=res.json())
            else:
                error_msg = f"Retrieving Github repo failed | status code: {str(res.status_code)} | response: {str(res)}"
                self.logger.warning(error_msg)
                output = dict(status="failed", error=error_msg)

            return output

        except Exception as e:
            self.logger.error(
                f"Unexpected error occured at {self.get_github_repo.__name__} | {str(e)}"
            )
            raise e

    async def get_github_repo_list(self, access_token: str):
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {access_token}",
            }
            host = "https://api.github.com/user/repos"

            res = self.requests.get(host, headers=headers)

            output: GetGitHubRepoListOutput

            if res.status_code == 200:
                self.logger.info(
                    f"List of GitHub repositories for authenticated user successfully returned"
                )
                output = dict(status="success", data=res.json())
            else:
                error_msg = f"Retrieving Github repos failed | status code: {str(res.status_code)} | response: {str(res)}"
                self.logger.warning(error_msg)
                output = dict(status="failed", error=error_msg)

            return output

        except Exception as e:
            self.logger.error(
                f"Unexpected error occured at {self.get_github_repo_list.__name__} | {str(e)}"
            )
            raise e

    async def register_push_github_repo(
        self, access_token: str, repo_fullname: str
    ) -> GitHubCallOutput:
        try:
            from config import GITHUB_WEBHOOK_CALLBACK

            if GITHUB_WEBHOOK_CALLBACK is None:
                raise Exception(
                    "GITHUB_WEBHOOK_CALLBACK cannot be None, check the env variable"
                )

            payload = {
                "hub.mode": "subscribe",
                "hub.topic": f"https://github.com/{repo_fullname}/events/push.json",
                "hub.callback": GITHUB_WEBHOOK_CALLBACK,
            }

            headers = {
                "Accept": "application/json",
                "Authorization": f"token {access_token}",
            }
            host = "https://api.github.com/hub"

            res = self.requests.post(host, headers=headers, data=payload)

            output: GitHubCallOutput

            if res.status_code == 204:
                self.logger.info(
                    f"GitHub webhook for push event successfully registered | {repo_fullname}"
                )
                output = dict(status="success")
            else:
                error_msg = f"GitHub webhook registration failed | status code: {str(res.status_code)} | repo name: {repo_fullname}"
                self.logger.warning(error_msg)
                output = dict(status="failed", error=error_msg)

            return output
        except Exception as e:
            self.logger.error(
                f"Error at {self.register_push_github_repo.__name__} | {str(e)}"
            )
            raise e

    async def get_github_repo_last_commit(
        self, access_token: str, full_name: str, branch: str
    ) -> GetGitHubRepoLastCommitOutput:
        try:
            headers = {
                "Accept": "application/vnd.github+json",
                "Authorization": f"token {access_token}",
            }

            # Get the branch detail to find the sha of the latest commit
            # https://docs.github.com/en/rest/branches/branches#get-a-branch
            host = f"https://api.github.com/repos/{full_name}/branches/{branch}"
            res = self.requests.get(host, headers=headers)

            output: GetGitHubRepoLastCommitOutput

            if res.status_code == 200:
                self.logger.info(
                    f"Last commit of GitHub repo has retrieved | repo: {full_name} | branch: {branch}"
                )
                data = res.json()
                commit = data["commit"]["sha"]
                output = dict(status="success", commit=commit)
            else:
                error_msg = f"Failed to retrieve the last commit of GitHub repo | status code: {str(res.status_code)} | repo: {full_name} | branch {branch}"
                self.logger.warning(error_msg)
                output = dict(status="failed", error=error_msg)

            return output
        except Exception as e:
            self.logger.error(
                f"Error at {self.get_github_repo_last_commit.__name__} | {str(e)}"
            )
            raise e
