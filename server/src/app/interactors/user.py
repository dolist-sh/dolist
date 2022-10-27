from app.domain.user import User

from infra.storage.userdb import UserDBAccess
from infra.integration.github import GitHubService, GetGitHubRepoOutput

from logging import Logger


class UserBaseUseCase:
    def __init__(
        self,
        userdb: UserDBAccess,
        github: GitHubService,
        logger: Logger,
    ) -> None:
        self.userdb = userdb
        self.github = github
        self.logger = logger


class GetUserUseCase(UserBaseUseCase):
    async def execute(self, email: str) -> User:
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


class GetUserGitHubReposUseCase(UserBaseUseCase):
    async def execute(self, email: str):
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


class UserInteractor:
    def __init__(
        self, get_user_github_repos: GetUserGitHubReposUseCase, get_user: GetUserUseCase
    ) -> None:
        self.get_user_github_repos = get_user_github_repos
        self.get_user = get_user
