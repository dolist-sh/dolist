"""Database access module for user."""

from uuid import UUID
from sqlalchemy import sql
from domain.user import User, CreateUserInput
from storage.model import user_schema
from storage.db import engine

user_db = user_schema
db = engine


def create_user(payload: CreateUserInput) -> User:
    try:
        # TODO: Add email unique check

        from uuid import uuid4

        new_id = uuid4()
        new_user_data = dict(id=new_id, **input)

        insert = user_db.insert()
        db.execute(insert, new_user_data)

        new_user_obj = self.read_user(new_id)

        return new_user_obj

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


def read_user(id: UUID) -> User:
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


def read_user_by_email(email: str) -> User:
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
