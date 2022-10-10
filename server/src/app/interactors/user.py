from app.domain.user import User

from infra.storage.userdb import UserDBAccess
from infra.integration.github import GitHubService, GetGitHubRepoOutput

from logging import Logger


class UserInteractor:
    def __init__(
        self,
        userdb: UserDBAccess,
        github: GitHubService,
        logger: Logger,
    ) -> None:
        self.userdb = userdb
        self.github = github
        self.logger = logger

    async def execute_get_user(self, email: str) -> User:
        try:
            user = await self.userdb.read_user_by_email(email)

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
            user = await self.userdb.read_user_by_email(email)
            github_token = user.oauth[0]["token"]  # TODO: Replace this with find call

            output: GetGitHubRepoOutput = await self.github.get_github_repo_list(
                github_token
            )

            if output["status"] == "success":
                return output["data"]
            else:
                raise ValueError(output["error"])
        except ValueError as e:
            raise e
        except Exception as e:
            raise e
