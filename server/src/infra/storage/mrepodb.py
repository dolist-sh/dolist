"""Database access module for MonitoredRepo."""

from time import time
from app.domain.mrepo import (
    MonitoredRepo,
    CreateMonitoredReposInput,
    AddParsedResultInput,
)

import sqlalchemy
from typing import List, Union
from uuid import UUID
from logging import Logger


class MonitoredRepoDBAccess:
    def __init__(
        self,
        sql_driver: sqlalchemy,
        db_instance: sqlalchemy.engine.Engine,
        mrepo_schema: sqlalchemy.Table,
        parsed_comment_schema: sqlalchemy.Table,
        logger: Logger,
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

            result = self.db_instance.execute(select).fetchone()

            if result is None:
                return None
            else:
                return MonitoredRepo(**result)
        except Exception as e:
            raise e

    async def read_monitored_repo(self, id: UUID) -> Union[MonitoredRepo, None]:
        try:
            select = self.mrepo_schema.select().where(self.mrepo_schema.c.id == id)

            result = self.db_instance.execute(select).fetchone()

            select_comments = self.parsed_comment_schema.select().where(
                self.parsed_comment_schema.c.mrepoId == id
            )
            comments = self.db_instance.execute(select_comments).fetchall()

            if result is None:
                return None
            else:
                return MonitoredRepo(**result, parsedComments=comments)

        except Exception as e:
            raise e

    async def read_monitored_repos(
        self, user_id: UUID, status, limit: int, offset: int
    ) -> List[MonitoredRepo]:
        try:
            select_mrepos = (
                self.mrepo_schema.select()
                .where(
                    self.sql_driver.and_(
                        self.mrepo_schema.c.userId == user_id,
                        self.mrepo_schema.c.status == status,
                    )
                )
                .limit(limit)
                .offset(offset)
            )

            mrepos = self.db_instance.execute(select_mrepos).fetchall()

            output = []

            for repo in mrepos:
                select_comments = self.parsed_comment_schema.select().where(
                    self.parsed_comment_schema.c.mrepoId == repo.id
                )
                comments = self.db_instance.execute(select_comments).fetchall()

                output.append(MonitoredRepo(**repo, parsedComments=comments))
            return output
        except Exception as e:
            raise e

    async def create_parse_report(
        self, last_commit: str, payload: AddParsedResultInput, mrepo_id: UUID
    ) -> None:
        conn = self.db_instance.connect()
        transaction = conn.begin()
        try:
            timestamp = int(time())

            # Writing lastCommit as it's not known at the object is written to the DB.
            update_last_commit_stmt = (
                self.mrepo_schema.update()
                .where(self.mrepo_schema.c.id == mrepo_id)
                .values(lastCommit=last_commit, lastUpdated=timestamp)
            )
            self.db_instance.execute(update_last_commit_stmt)

            # Add id field to parsed comments from the payload
            mapped_result = []

            for item in payload["parseResult"]:
                item["id"] = self._generate_parsed_comment_id(
                    item["type"],
                    item["title"],
                    item["path"],
                    item["lineNumber"],
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

            resolved_comments = self._find_resolved_comments(
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
            new_comments_from_payload = self._find_new_comments(
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
            raise e

    def _generate_parsed_comment_id(
        self, type: str, title: str, file_path: str, line_number: int
    ):
        import hashlib

        hash_payload = bytes(
            f"{type}, {title}, {file_path}, {line_number}", encoding="utf-8"
        )

        return hashlib.sha1(hash_payload).hexdigest()

    def _find_resolved_comments(
        self, prev_comments_from_db: List, parsed_comments: List
    ) -> List:
        """
        When a comment is in prev_comments from DB, but not in parsed_comments, it's resolved.
        """

        def _is_resolved_comment(id: str) -> bool:
            result = True
            for parsed_comment in parsed_comments:
                if id == parsed_comment["id"]:
                    result = False
                    break
            return result

        resolved = [
            comment
            for comment in prev_comments_from_db
            if _is_resolved_comment(comment["id"]) is True
        ]

        return resolved

    def _find_new_comments(
        self, prev_comments_from_db: List, parsed_comments: List
    ) -> List:
        """
        When a comment is in parsed_comments, but not in prev_comments_from_db, it's a new comment
        """

        def _is_new_comment(id: str):
            result = True
            for comment_from_db in prev_comments_from_db:
                if id == comment_from_db["id"]:
                    result = False
                    break
            return result

        new = [
            comment
            for comment in parsed_comments
            if _is_new_comment(comment["id"]) is True
        ]

        return new
