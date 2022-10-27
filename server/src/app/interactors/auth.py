from app.domain.auth import CreateMachineTokenInput, MachineToken

from infra.auth.github import GitHubOAuthService
from infra.storage.userdb import UserDBAccess
from infra.auth.jwt import JWTService


class AuthBaseUseCase:
    def __init__(
        self,
        userdb: UserDBAccess,
        github_auth: GitHubOAuthService,
        jwt: JWTService,
    ) -> None:
        self.userdb = userdb
        self.github_auth = github_auth
        self.jwt = jwt


class GitHubAuthUseCase(AuthBaseUseCase):
    async def execute(self, session_code: str):
        try:
            github_token = await self.github_auth.get_github_access_token(session_code)

            if github_token is None:
                raise ValueError("Invalid session code")

            github_user = await self.github_auth.get_github_user(github_token)

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
            email = await self.github_auth.get_github_user_email(
                github_username, github_token
            )

            user_check_result = await self.userdb.read_user_by_email(email)

            oauth_payload = dict(type="github", token=github_token)

            if user_check_result is None:
                """Sign-up case"""
                user_payload = dict(
                    email=email,
                    name=name,
                    profileUrl=profile_url,
                    oauthInUse=oauth_payload,
                )

                await self.userdb.create_user(user_payload)

                return self.jwt.issue_token(user_payload["email"])

            else:
                """Sign-in case"""
                await self.userdb.write_github_token(email, github_token)

                return self.jwt.issue_token(user_check_result.email)
        except ValueError as e:
            raise e
        except Exception as e:
            raise e


class WorkerAuthUseCase(AuthBaseUseCase):
    async def execute(self, payload: CreateMachineTokenInput) -> MachineToken:
        try:
            from config import WORKER_OAUTH_CLIENT_ID, WORKER_OAUTH_CLIENT_SECRET

            client_id = payload["client_id"]
            client_secret = payload["client_secret"]

            if (client_id != WORKER_OAUTH_CLIENT_ID) or (
                client_secret != WORKER_OAUTH_CLIENT_SECRET
            ):
                raise ValueError("Invalid auth request")

            return self.jwt.issue_machine_token(payload)
        except ValueError as e:
            raise e
        except Exception as e:
            raise e


class AuthInteractor:
    def __init__(
        self, auth_github: GitHubAuthUseCase, auth_worker: WorkerAuthUseCase
    ) -> None:
        self.auth_github = auth_github
        self.auth_worker = auth_worker
