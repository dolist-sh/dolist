import requests


async def get_github_repos(access_token: str):
    try:
        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {access_token}",
        }
        host = "https://api.github.com/user/repos"

        res = requests.get(host, headers=headers)

        return res.json()

    except Exception as e:
        raise e
