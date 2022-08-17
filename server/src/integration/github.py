import requests
from helpers.logger import logger

from typing import Union
from typing_extensions import Literal, TypedDict


async def get_github_repos(access_token: str):
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}",
        }
        host = "https://api.github.com/user/repos"

        res = requests.get(host, headers=headers)

        # TODO: Check the response code and throw exception
        return res.json()

    except Exception as e:
        logger.error(f"Unexpected issue at {get_github_repos.__name__} | {str(e)}")
        raise e


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
            output = dict(status="success")
        else:
            error_msg = f"Github webhook registration failed | status code: {str(res.status_code)} | response: {str(res)}"
            output = dict(status="failed", error=error_msg)

        return output
    except Exception as e:
        logger.error(
            f"Unexpected error occured at {register_push_github_repos.__name__} | {str(e)}"
        )
