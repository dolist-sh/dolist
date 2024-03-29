import requests


class GitHubOAuthService:
    def __init__(self, requests: requests) -> None:
        self.requests = requests

    async def get_github_access_token(self, session_code: str) -> str:
        from config import (
            GITHUB_OAUTH_CLIENT_ID,
            GITHUB_OAUTH_CLIENT_SECRET,
        )

        try:
            payload = {
                "client_id": GITHUB_OAUTH_CLIENT_ID,
                "client_secret": GITHUB_OAUTH_CLIENT_SECRET,
                "code": session_code,
            }

            headers = {"Accept": "application/json"}
            host = "https://github.com/login/oauth/access_token/"

            res = self.requests.post(host, headers=headers, params=payload)
            data = res.json()

            return data["access_token"]

        except KeyError as e:
            """When no access_token is returned from Github, data['access_token'] will throw KeyError"""
            return None
        except Exception as e:
            raise e

    async def get_github_user(self, access_token: str):
        try:
            headers = {"Authorization": f"token {access_token}"}
            host = "https://api.github.com/user"

            res = self.requests.get(host, headers=headers)

            return res.json()

        except Exception as e:
            raise e

    async def get_github_user_email(self, username: str, access_token: str) -> str:
        """GitHub API doc: https://docs.github.com/en/rest/users/emails"""
        try:
            username = username
            password = access_token

            host = "https://api.github.com/user/emails"

            res = self.requests.get(host, auth=(username, password))

            data = res.json()
            primary_email = [x for x in data if x["primary"] is True]

            return primary_email[0]["email"]

        except KeyError as e:
            return None
        except Exception as e:
            raise e
