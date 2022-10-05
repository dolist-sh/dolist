"""Database access module for MonitoredRepo."""
from infra.storage.model import monitored_repo_schema, parsed_comment_schema
from infra.storage.db import engine

from app.domain.mrepo import (
    MonitoredRepo,
    CreateMonitoredReposInput,
    AddParsedResultInput,
    generate_parsed_comment_id,
    _find_resolved_comments,
    _find_new_comments,  # TODO: Think about where to place this domain logics -> should this be part of DB access?
)

import sqlalchemy

from uuid import UUID
from time import time
from logger import logger

from typing import Union


class MonitoredRepoDBAdaptor:
    def __init__(
        self,
        sql_driver: sqlalchemy,
        db_instance: engine,
        mrepo_schema: monitored_repo_schema,
        parsed_comment_schema: parsed_comment_schema,
        logger: logger,
    ) -> None:
        self.sql_driver = sql_driver
        self.db_instance = db_instance
        self.mrepo_schema = mrepo_schema
        self.parsed_comment_schema = parsed_comment_schema
        self.logger = logger

    async def create_monitored_repo(
        self, payload: CreateMonitoredReposInput, user_id: UUID
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

            insert = self.mrepo_schema.insert()
            self.db_instance.execute(insert, new_monitored_repo_data)

            new_monitored_repo_obj = await self.read_monitored_repo(new_id)

            return new_monitored_repo_obj
        except Exception as e:
            self.logger.critical(f"Unexpected exceptions: {str(e)}")
            raise e

    async def read_monitored_repo_by_fullname(
        self, full_name: str, provider: str
    ) -> Union[MonitoredRepo, None]:
        try:
            select = self.mrepo_schema.select().where(
                self.sql_driver.sql.and_(
                    self.mrepo_schema.c.provider == provider,
                    self.mrepo_schema.c.fullName == full_name,
                )
            )

            repo = self.db_instance.execute(select).fetchone()

            return repo
        except Exception as e:
            self.logger.critical(f"Unexpected exceptions: {str(e)}")
            raise e

    async def read_monitored_repo(self, id: UUID) -> MonitoredRepo:
        try:
            select = self.mrepo_schema.select().where(self.mrepo_schema.c.id == id)

            result = self.db_instance.execute(select).fetchone()

            if result is None:
                return None
            else:
                return MonitoredRepo(**result)

        except Exception as e:
            self.logger.critical(f"Unexpected exceptions: {str(e)}")
            raise e

    # TODO: Write test for different scenarios with this methods
    async def create_parse_report(
        self, last_commit: str, payload: AddParsedResultInput
    ) -> None:
        conn = self.db_instance.connect()
        transaction = conn.begin()
        try:
            mrepo_id = payload["mrepoId"]
            timestamp = int(time())

            # Below update is due to the lastCommit field at the MonitoredRepo object is not known when it's first written to DB
            update_last_commit_stmt = (
                self.mrepo_schema.update()
                .where(self.mrepo_schema.c.id == mrepo_id)
                .values(lastCommit=last_commit, lastUpdated=timestamp)
            )
            self.db_instance.execute(update_last_commit_stmt)

            # Add id field to parsed comments from the payload
            mapped_result = []

            for item in payload["parseResult"]:
                item["id"] = generate_parsed_comment_id(
                    item["type"],
                    item["title"],
                    item["path"],
                )
                mapped_result.append(item)

            # Load all previously parsed comments from DB
            load_parsed_comments = self.parsed_comment_schema.select().where(
                self.parsed_comment_schema.c.mrepoId == mrepo_id
            )
            prev_parsed_comments = self.db_instance.execute(
                load_parsed_comments
            ).fetchall()

            new_from_prev_parsed_comments = [
                c for c in prev_parsed_comments if c["status"] == "New"
            ]

            if len(new_from_prev_parsed_comments) > 0:
                self.logger.info(
                    "Previously parsed comments have comments with status - New"
                )
                self.logger.info(
                    "Updating the status to Normal in favor of new parsed result"
                )

                # Mark previously new comments from DB to normal
                update_from_new_to_normal_stmt = (
                    self.parsed_comment_schema.update()
                    .where(self.parsed_comment_schema.c.status == "New")
                    .values(status="Normal", lastUpdated=timestamp)
                )
                self.db_instance.execute(update_from_new_to_normal_stmt)

            resolved_comments = _find_resolved_comments(
                prev_parsed_comments, mapped_result
            )

            if len(resolved_comments) > 0:
                self.logger.info("Resolved comment found from payload")
                self.logger.info(resolved_comments)

                # Change the status of resolved comment in DB
                update_to_resolved_stmt = (
                    self.parsed_comment_schema.update()
                    .where(
                        self.parsed_comment_schema.c.id
                        == self.sql_driver.bindparam("comment_id")
                    )
                    .values(status="Resolved", lastUpdated=timestamp)
                )
                update_to_resolved_payload = [
                    {"comment_id": c["id"]} for c in resolved_comments
                ]
                self.db_instance.execute(
                    update_to_resolved_stmt, update_to_resolved_payload
                )

            # Find comments from payload that doesn't exist yet in the DB
            new_comments_from_payload = _find_new_comments(
                prev_parsed_comments, mapped_result
            )
            if len(new_comments_from_payload):
                self.logger.info("New comments found from payload...")
                self.logger.info("Inserting to the database...")
                self.logger.info(new_comments_from_payload)

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
                self.db_instance.execute(
                    self.parsed_comment_schema.insert(), new_comments_insert_payload
                )

            # TODO: Mark neutral comment older than certain duration to old (threshold tbd)

            transaction.commit()
            return
        except Exception as e:
            transaction.rollback()
            self.logger.error(
                f"Unexpected exceptions at {self.create_parse_report.__name__}: {str(e)}"
            )
            raise e
