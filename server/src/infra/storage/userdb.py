"""Database access module for User."""

from app.domain.user import User, CreateUserInput
from uuid import UUID
from sqlalchemy import Table
from sqlalchemy.engine import Engine


class UserDBAdaptor:
    def __init__(self, db_instance: Engine, user_schema: Table) -> None:
        self.db_instance = db_instance
        self.user_schema = user_schema

    async def create_user(self, payload: CreateUserInput) -> User:
        try:
            from time import time
            from uuid import uuid4

            # TODO: Add email unique check in this call

            new_id = uuid4()
            oauth = [payload["oauthInUse"]]
            timestamp = int(time())

            """
                # TODO: More user type could be added
                # Instead of hard-coded value for the type field, take the value from input when more user type need to be supported.
            """

            new_user_data = dict(
                id=new_id, type="admin", oauth=oauth, createdAt=timestamp, **payload
            )

            insert = self.user_schema.insert()
            self.db_instance.execute(insert, new_user_data)

            new_user_obj = await self.read_user(new_id)

            return new_user_obj

        except Exception as e:
            raise e

    async def write_github_token(self, email: str, new_token: str) -> str:
        try:
            oauth = dict(type="github", token=new_token)

            # TODO: oauth list should be re-constructred
            update = (
                self.user_schema.update()
                .where(self.user_schema.c.email == email)
                .values(oauth=[oauth])
            )
            self.db_instance.execute(update)

            updated_user = await self.read_user_by_email(email)

            return updated_user.oauth[0]["token"]

        except Exception as e:
            raise e

    async def read_user(self, id: UUID) -> User:
        try:
            select = self.user_schema.select().where(self.user_schema.c.id == id)

            result = self.db_instance.execute(select).fetchone()

            if result is None:
                return None
            else:
                return User(**result)

        except Exception as e:
            raise e

    async def read_user_by_email(self, email: str) -> User:
        try:
            select = self.user_schema.select().where(self.user_schema.c.email == email)

            result = self.db_instance.execute(select).fetchone()

            if result is None:
                return None
            else:
                return User(**result)

        except Exception as e:
            raise e
