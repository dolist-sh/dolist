from app.domain.user import User

from infra.storage.userdb import read_user_by_email
from infra.integration.github import get_github_repo_list


class UserInteractor:
    def __init__(self) -> None:
        # infra.storage.userdb
        # infra.integration.github
        pass

    async def execute_get_user(self, email: str) -> User:
        try:
            user = await read_user_by_email(email)

            if user is None:
                raise ValueError("User not found")
            else:
                return user
        except ValueError as e:
            raise e
        except Exception as e:
            raise e

    async def execute_get_user_github_repos(self, email: str):
        try:
            user = await read_user_by_email(email)
            github_token = user.oauth[0]["token"]  # TODO: Replace this with find call

            from src.infra.integration.github import GetGitHubRepoOutput

            output: GetGitHubRepoOutput = await get_github_repo_list(github_token)

            if output["status"] == "success":
                return output["data"]
            else:
                raise ValueError(output["error"])
        except ValueError as e:
            raise e
        except Exception as e:
            raise e
