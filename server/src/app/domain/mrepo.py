from uuid import UUID
from pydantic import BaseModel
from typing import List, Union, Optional
from typing_extensions import Literal, TypedDict


class CreateMonitoredReposInput(TypedDict):
    name: str
    fullName: str
    defaultBranch: str
    language: str
    url: str
    provider: Literal["github"]
    visibility: Literal["private", "public"]


class AddMonitoredReposInput(BaseModel):
    repos: List[CreateMonitoredReposInput]


class ParsedComment(BaseModel):
    id: str  # SHA-1 checksum
    mrepoId: UUID
    title: str
    type: Literal["TODO"]
    status: Literal["New", "Old", "Normal", "Resolved"]
    commentStyle: Literal["oneline", "multiline"]
    fullComment: List[str]
    filePath: str
    lineNumber: int
    createdAt: int
    lastUpdated: int


class MonitoredRepo(BaseModel):
    id: UUID  # uuid v4
    name: str
    fullName: str
    defaultBranch: str
    userId: UUID
    defaultBranch: str
    language: Optional[str]
    lastCommit: Optional[str]
    provider: Literal["github"]
    visibility: Literal["private", "public"]
    status: Literal["active", "inactive"]
    parsedComments: Optional[List[ParsedComment]]
    createdAt: int  # Unix timestamp
    lastUpdated: int  # Unix timestamp


class AddParsedResultInput(BaseModel):
    mrepoId: Union[str, UUID]
    parseResult: List[str]
