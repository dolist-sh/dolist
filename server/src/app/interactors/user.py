from app.domain.user import User

from infra.storage.userdb import read_user_by_email


class UserInteractor:
    def __init__(self) -> None:
        # infra.storage.userdb
        pass

    async def execute_get_user(email: str) -> User:
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
