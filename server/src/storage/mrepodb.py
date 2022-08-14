"""Database access module for MonitoredRepo."""

from uuid import UUID
from time import time
from sqlalchemy import sql
from storage.model import monitored_repo_schema
from storage.db import engine

from domain.mrepo import MonitoredRepo, CreateMonitoredReposInput

mrepo_db = monitored_repo_schema
db = engine


async def create_monitored_repo(
    payload: CreateMonitoredReposInput, user_id: UUID
) -> MonitoredRepo:
    try:
        from uuid import uuid4

        new_id = uuid4()
        timestamp = int(time())

        new_monitored_repo_data = dict(
            id=new_id,
            fullName=payload["fullName"],
            userId=user_id,
            provider=payload["provider"],
            status="active",
            createdAt=timestamp,
            lastUpdated=timestamp,
        )

        insert = mrepo_db.insert()
        db.execute(insert, new_monitored_repo_data)

        new_monitored_repo_obj = await read_monitored_repo(new_id)

        return new_monitored_repo_obj
    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e


async def read_monitored_repo(id: UUID) -> MonitoredRepo:
    try:
        select = mrepo_db.select().where(mrepo_db.c.id == id)

        result = db.execute(select).fetchone()

        if result is None:
            return None
        else:
            return MonitoredRepo(**result)

    except Exception as e:
        print(f"Unexpected exceptions: {str(e)}")
        raise e
