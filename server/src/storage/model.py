"""Schema definition for postgres"""

from sqlalchemy import MetaData, Table, Column, String, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID

import uuid

from .db import engine

metadata_obj = MetaData()

user_schema = Table(
    "users",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4()),
    Column("type", String(10), nullable=False),
    Column("email", String(50), nullable=False),
    Column("name", String(100), nullable=True),
    Column("profileUrl", String(100), nullable=False),
    Column("oauth", JSON, default=[]),
    Column("createdAt", Integer, nullable=False),
)

monitoredrepo_schema = Table(
    "monitoredrepo",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4()),
    Column("fullName", string(50), nullable=False),
    Column("userId", UUID(as_uuid=True), nullable=False),
    Column("provider", string(30), nullable=False),
    Column("status", string(20), nullable=False),
    Column("createdAt", Integer, nullable=False),
    Column("lastUpdated", Integer, nullable=False),
)


# Create a new table if doens't exist
user_schema.create(engine, checkfirst=True)
monitoredrepo_schema.create(engine, checkfirst=True)
