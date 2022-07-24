import requests

async def get_github_repos(access_token: str):
    try:
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github+json",
        }
        host = "https://api.github.com/user/repos"

        res = requests.get(host, headers)

        return res.json()

    except Exception as e:
        raise e
