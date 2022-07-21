"""Database access module for user."""

from uuid import UUID
from sqlalchemy import sql
from domain.user import User, CreateUserInput
from infra.model import user_schema
from infra.db import engine

# TODO: Write input model and return type
def create_user(payload: CreateUserInput) -> User:
    pass


def get_user_by_email(email) -> User:
    pass
