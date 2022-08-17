import requests
from logger import logger

from typing import Union, List
from typing_extensions import Literal, TypedDict


class GetGitHubReposOutput(TypedDict):
    status: Literal["success", "failed"]
    data: List[str]  # List of JSON
    error: Union[str, None]


async def get_github_repos(access_token: str):
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}",
        }
        host = "https://api.github.com/user/repos"

        res = requests.get(host, headers=headers)

        output: RegisterPushGitHubRepoOutput

        if res.status_code == 200:
            logger.info(
                f"List of GitHub repositories for authenticated user successfully returned"
            )
            output = dict(status="success", data=res.json())
        else:
            error_msg = f"Retrieving Github repos failed | status code: {str(res.status_code)} | response: {str(res)}"
            logger.warning(error_msg)
            output = dict(status="failed", error=error_msg)

        return output

    except Exception as e:
        logger.error(
            f"Unexpected error occured at {get_github_repos.__name__} | {str(e)}"
        )


class RegisterPushGitHubRepoOutput(TypedDict):
    status: Literal["success", "failed"]
    error: Union[str, None]


async def register_push_github_repos(
    access_token: str, repo_fullname: str
) -> RegisterPushGitHubRepoOutput:
    try:
        payload = {
            "hub.mode": "subscribe",
            "hub.topic": f"https://github.com/{repo_fullname}/events/push.json",
            "hub.callback": "http://15.188.137.121/api/webhook",
        }

        headers = {
            "Accept": "application/json",
            "Authorization": f"token {access_token}",
        }
        host = f"https://api.github.com/hub"

        res = requests.post(host, headers=headers, data=payload)

        output: RegisterPushGitHubRepoOutput

        if res.status_code == 204:
            logger.info(
                f"GitHub webhook for push event successfully registered | {repo_fullname}"
            )
            output = dict(status="success")
        else:
            error_msg = f"Github webhook registration failed | status code: {str(res.status_code)} | repo name: {repo_fullname}"
            logger.warning(error_msg)
            output = dict(status="failed", error=error_msg)

        return output
    except Exception as e:
        logger.error(f"Error at {register_push_github_repos.__name__} | {str(e)}")
        raise e
