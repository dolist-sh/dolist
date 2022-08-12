"""Database access module for User."""

from uuid import UUID
from time import time
from sqlalchemy import sql
from domain.user import User, CreateUserInput
from storage.model import user_schema
from storage.db import engine

user_db = user_schema
db = engine


async def create_user(payload: CreateUserInput) -> User:
    # TODO: Add email unique check in this call
    try:
        from uuid import uuid4

        new_id = uuid4()
        oauth = [payload["oauthInUse"]]
        timestamp = int(time())

        # TODO: Create different user type based on the arg
        new_user_data = dict(
            id=new_id, type="admin", oauth=oauth, createdAt=timestamp, **payload
        )

        insert = user_db.insert()
        db.execute(insert, new_user_data)

        new_user_obj = await read_user(new_id)

        return new_user_obj

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


async def write_github_token(email: str, new_token: str) -> str:
    try:
        oauth = dict(type="github", token=new_token)

        # TODO: oauth list should be re-constructred
        update = user_db.update().where(user_db.c.email == email).values(oauth=[oauth])
        db.execute(update)

        updated_user = await read_user_by_email(email)

        return updated_user.oauth[0]["token"]

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


async def read_user(id: UUID) -> User:
    try:
        select = user_db.select().where(user_db.c.id == id)

        result = db.execute(select).fetchone()

        if result is None:
            return None
        else:
            return User(**result)

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


async def read_user_by_email(email: str) -> User:
    try:
        select = user_db.select().where(user_db.c.email == email)

        result = db.execute(select).fetchone()

        if result is None:
            return None
        else:
            return User(**result)

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e
