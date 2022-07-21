import requests

from config import (
    GITHUB_OAUTH_CLIENT_ID,
    GITHUB_OAUTH_CLIENT_SECRET,
    GITHUB_OAUTH_CONFIRM_URI,
)


async def get_github_access_token(session_code: str):
    try:
        payload = {
            "client_id": GITHUB_OAUTH_CLIENT_ID,
            "client_secret": GITHUB_OAUTH_CLIENT_SECRET,
            "redirect_uri": GITHUB_OAUTH_CONFIRM_URI,
            "code": session_code,
        }

        headers = {"Accept": "application/json"}
        host = "https://github.com/login/oauth/access_token/"

        res = requests.post(host, headers=headers, params=payload)

        return res.json()
    except e:
        raise e


async def get_github_user(access_token):
    try:
        headers = {"Authorization": f"token {access_token}"}
        host = "https://api.github.com/user"

        res = requests.get(host, headers=headers)

        return res.json()
    except e:
        raise e


async def get_github_user_email(username: str, access_token: str) -> str:
    """GitHub API doc: https://docs.github.com/en/rest/users/emails"""
    try:
        username = username
        password = access_token

        host = "https://api.github.com/user/emails"

        res = requests.get(host, auth=(username, password))

        data = res.json()
        primary_email = [x for x in data if x["primary"] is True]

        return primary_email[0]["email"]
    except e:
        raise e
