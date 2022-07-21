"""Schema definition for postgres"""

from sqlalchemy import MetaData, Table, Column, String, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID

import uuid

from .db import engine

metadata_obj = MetaData()

user_schema = Table(
    "user",
    metadata_obj,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4()),
    Column("type", String(10), nullable=False),
    Column("email", String(50), nullable=False),
    Column("name", String(100), nullable=False),
    Column("profileUrl", String(100), nullable=False),
    Column("oauth", JSON, default=[]),
    Column("createdAt", Integer, nullable=False),
)

# Create a new table if doens't exist
user_schema.create(engine, checkfirst=True)
