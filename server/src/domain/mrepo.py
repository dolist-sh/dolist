from uuid import UUID
from pydantic import BaseModel
from typing import List
from typing_extensions import Literal, TypedDict


class CreateMonitoredReposInput(TypedDict):
    fullName: str
    provider: Literal["github"]


class AddMonitoredReposInput(BaseModel):
    repos: List[CreateMonitoredReposInput]


class MonitoredRepo(BaseModel):
    id: UUID  # uuid v4
    fullName: str
    userId: UUID
    provider: Literal["github"]
    status: Literal["active", "inactive"]
    createdAt: int  # Unix timestamp
    lastUpdated: int  # Unix timestamp
