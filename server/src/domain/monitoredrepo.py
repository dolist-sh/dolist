from uuid import UUID
from pydantic import BaseModel
from typing_extensions import Literal


class MonitoredRepo(BaseModel):
    id: UUID  # uuid v4
    fullName: str
    userId: UUID
    provider: Literal["github"]
    status: Literal["active", "inactive"]
    createdAt: int  # Unix timestamp
    lastUpdated: int  # Unix timestamp
