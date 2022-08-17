import requests
from typing_extensions import Literal


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
        print(str(e))
        raise e


async def register_push_github_repos(
    access_token: str, repo_fullname: str
) -> Literal["success"]:
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

        if res.status_code != 204:
            raise Exception(
                f"Github webhook registration failed | status code: {str(res.status_code)}"
            )

        return "success"
    except Exception as e:
        print(str(e))
        raise e
