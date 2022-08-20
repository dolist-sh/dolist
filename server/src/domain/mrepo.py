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


class AddParsedResultInput(BaseModel):
    mrepoId: Union[str, UUID]
    parseResult: List[str]


def generate_parsed_comment_id(type: str, title: str, filePath: str, lineNumber: int):
    import hashlib

    hash_payload = bytes(f"{type}, {title}, {filePath}, {lineNumber}", encoding="utf-8")

    return hashlib.sha1(hash_payload).hexdigest()


# TODO: Add typing and move to storage class
def _find_resolved_comments(prev_comments_from_db: List, parsed_comments: List) -> List:
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


# TODO add typing and move to the storage class
def _find_new_comments(prev_comments_from_db: List, parsed_comments: List) -> List:
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
        comment for comment in parsed_comments if _is_new_comment(comment["id"]) is True
    ]

    return new


class ParsedComment(BaseModel):
    id: UUID  # This field should be a checksum
    title: str
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
    lastCommit: Optional[str]
    provider: Literal["github"]
    visibility: Literal["private", "public"]
    status: Literal["active", "inactive"]
    parsedComments: Optional[List[ParsedComment]]
    createdAt: int  # Unix timestamp
    lastUpdated: int  # Unix timestamp
