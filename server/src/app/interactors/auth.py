from infra.auth.github import (
    get_github_access_token,
    get_github_user,
    get_github_user_email,
)
from infra.storage.userdb import read_user_by_email, create_user, write_github_token
from infra.auth.jwt import issue_token


class AuthInteractor:
    def __init__(self) -> None:
        # infra.storage.userdb
        # infra.integration.github
        # infra.auth.github
        # infra.auth.jwt
        pass

    async def execute_github_auth(self, session_code: str):
        try:
            github_token = await get_github_access_token(session_code)

            if github_token is None:
                raise ValueError("Invalid session code")

            github_user = await get_github_user(github_token)

            email = github_user["email"]
            name = github_user["name"]
            profile_url = github_user["avatar_url"]
            github_username = github_user["login"]

            if email is None:
                """
                Fetch email address for user who marked their email as private.
                This step is requred as email field from get_github_user method returns null,
                When user have marked their email private.
                """
            email = await get_github_user_email(github_username, github_token)

            user_check_result = await read_user_by_email(email)

            oauth_payload = dict(type="github", token=github_token)

            if user_check_result is None:
                """Sign-up case"""
                user_payload = dict(
                    email=email,
                    name=name,
                    profileUrl=profile_url,
                    oauthInUse=oauth_payload,
                )

                await create_user(user_payload)

                return issue_token(user_payload["email"])

            else:
                """Sign-in case"""
                await write_github_token(email, github_token)

                return issue_token(user_check_result.email)
        except ValueError as e:
            raise e
        except Exception as e:
            raise e
