from app.domain.user import User
from app.domain.mrepo import AddMonitoredReposInput, MonitoredRepo
from typing import List

from infra.storage.userdb import read_user_by_email
from infra.integration.github import (
    get_github_repo_list,
    get_github_repo,
    register_push_github_repo,
)
from infra.storage.mrepodb import read_monitored_repo_by_fullname, create_monitored_repo
from logger import logger


class UserInteractor:
    def __init__(self) -> None:
        # infra.storage.userdb
        # infra.storage.mrepodb
        # infra.integration.github
        # logger
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

    async def execute_add_monitored_repos(
        self, email: str, payload: AddMonitoredReposInput
    ) -> List[MonitoredRepo]:
        try:
            user = await read_user_by_email(email)
            user_id = user.id

            new_monitroed_repos: List[MonitoredRepo] = []
            oauth_token = user.oauth[0]["token"]

            if len(payload["repos"]) > 0:
                for repo in payload["repos"]:

                    repo = dict(repo)
                    github_repo_check = await get_github_repo(
                        oauth_token, repo["fullName"]
                    )

                    if github_repo_check["status"] == "fail":
                        logger.warning(
                            f"Non-existing GitHub repository was requested for monitoring | user_id: {user_id} | repo_fullname: {repo['fullName']}"
                        )

                    if github_repo_check["status"] == "success":
                        duplication_check_result = (
                            await read_monitored_repo_by_fullname(
                                repo["fullName"], "github"
                            )
                        )

                        if duplication_check_result is None:
                            """Adding a new repository"""
                            new_repo = await create_monitored_repo(repo, user_id)
                            new_monitroed_repos.append(new_repo)
                            await register_push_github_repo(
                                oauth_token, repo["fullName"]
                            )
                        else:
                            """Skipping as it's already monitored repository"""
                            logger.warning(
                                f"Already monitored repository was included in the | user_id: {user_id} | repo_name: {repo['fullName']}"
                            )

            return new_monitroed_repos

        except Exception as e:
            raise e
