from uuid import UUID
from pydantic import BaseModel
from typing import List, Union
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


class AddParsedResultInput(BaseModel):
    mrepoId: Union[str, UUID]
    parseResult: List[str]


class ParsedComment(BaseModel):
    id: UUID  # This field should be a checksum
    type: Literal["TODO"]
    status: Literal["New", "Old", "Normal", "Resolved"]
    commentStyle: Literal["oneline", "multiline"]
    fullComment: List[str]
    filePath: str
    lineNumber: int


class MonitoredRepo(BaseModel):
    id: UUID  # uuid v4
    name: str
    fullName: str
    defaultBranch: str
    language: str
    userId: UUID
    defaultBranch: str
    lastCommit: str
    provider: Literal["github"]
    visibility: Literal["private", "public"]
    status: Literal["active", "inactive"]
    parsedComments: List[ParsedComment]
    createdAt: int  # Unix timestamp
    lastUpdated: int  # Unix timestamp
