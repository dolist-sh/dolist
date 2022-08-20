"""Database access module for MonitoredRepo."""

from sqlalchemy import bindparam
from sqlalchemy.sql import and_
from storage.model import monitored_repo_schema, parsed_comment_schema
from storage.db import engine

from domain.mrepo import (
    MonitoredRepo,
    CreateMonitoredReposInput,
    AddParsedResultInput,
    generate_parsed_comment_id,
    _find_resolved_comments,
    _find_new_comments,
)
from uuid import UUID
from time import time
from logger import logger

from typing import Union

mrepo_db = monitored_repo_schema
parsed_comment_db = parsed_comment_schema
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
            name=payload["name"],
            fullName=payload["fullName"],
            defaultBranch=payload["defaultBranch"],
            language=payload["language"],
            userId=user_id,
            provider=payload["provider"],
            visibility=payload["visibility"],
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


async def read_monitored_repo_by_fullname(
    full_name: str, provider: str
) -> Union[MonitoredRepo, None]:
    try:
        select = mrepo_db.select().where(
            and_(mrepo_db.c.provider == provider, mrepo_db.c.fullName == full_name)
        )

        repo = db.execute(select).fetchone()

        return repo
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


# TODO: Write test for different scenarios with this methods
async def create_parse_report(last_commit: str, payload: AddParsedResultInput) -> None:
    conn = db.connect()
    transaction = conn.begin()
    try:
        mrepo_id = payload["mrepoId"]
        timestamp = int(time())

        # Below update is due to the lastCommit field at the MonitoredRepo object is not known when it's first written to DB
        update_last_commit_stmt = (
            mrepo_db.update()
            .where(mrepo_db.c.id == mrepo_id)
            .values(lastCommit=last_commit, lastUpdated=timestamp)
        )
        db.execute(update_last_commit_stmt)

        # Add id field to parsed comments from the payload
        mapped_result = []

        for item in payload["parseResult"]:
            item["id"] = generate_parsed_comment_id(
                item["type"], item["title"], item["path"], item["lineNumber"]
            )
            mapped_result.append(item)

        # Load all previously parsed comments from DB
        load_parsed_comments = parsed_comment_db.select().where(
            parsed_comment_db.c.mrepoId == mrepo_id
        )
        prev_parsed_comments = db.execute(load_parsed_comments).fetchall()

        resolved_comments = _find_resolved_comments(prev_parsed_comments, mapped_result)

        if len(resolved_comments) > 0:
            print("Resolved comment found from payload")
            print(resolved_comments)

            # Change the status of resolved comment in DB
            update_to_resolved_stmt = (
                parsed_comment_db.update()
                .where(parsed_comment_db.c.id == bindparam("id"))
                .values(status="Resolved", lastUpdated=timestamp)
            )
            update_to_resolved_payload = [{"id": c["id"]} for c in resolved_comments]
            db.execute(update_to_resolved_stmt, update_to_resolved_payload)

        new_from_prev_parsed_comments = [
            c for c in prev_parsed_comments if c["status"] == "New"
        ]

        if len(new_from_prev_parsed_comments) > 0:
            print("Previously parsed comments have comments with status - New")
            print("Updating the status to Normal in favor of new parsed result")

            # Mark previously new comments from DB to normal
            update_from_new_to_normal_stmt = (
                parsed_comment_db.update()
                .where(parsed_comment_db.c.status == "New")
                .values(status="Normal", lastUpdated=timestamp)
            )
            db.execute(update_from_new_to_normal_stmt)

        # Find comments from payload that doesn't exist yet in the DB
        new_comments_from_payload = _find_new_comments(
            prev_parsed_comments, mapped_result
        )
        if len(new_comments_from_payload):
            print("New comments found from payload")
            print("Interesting to the database")
            print(new_comments_from_payload)
            new_comments_insert_payload = [
                {
                    "id": c["id"],
                    "mrepoId": mrepo_id,
                    "title": c["title"],
                    "type": c["type"],
                    "status": "New",
                    "commentStyle": c["commentStyle"],
                    "fullComment": c["fullComment"],
                    "filePath": c["path"],
                    "lineNumber": c["lineNumber"],
                    "createdAt": timestamp,
                    "lastUpdated": timestamp,
                }
                for c in new_comments_from_payload
            ]
            # Write all new comments from payload to DB
            db.execute(parsed_comment_db.insert(), new_comments_insert_payload)

        # Mark neutral comment older than certain duration to old (threshold tbd)
        # Update the last updated timestamps

        transaction.commit()
        return
    except Exception as e:
        transaction.rollback()
        logger.error(
            f"Unexpected exceptions at {create_parse_report.__name__}: {str(e)}"
        )
        raise e
