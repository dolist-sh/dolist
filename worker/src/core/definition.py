from typing import TypedDict
from typing_extensions import TypedDict, Literal


class ParseRequestMsg(TypedDict):
    userId: str
    token: str
    repoName: str
    branch: str
    provider: Literal["github"]


class ParseCompleteMsg(TypedDict):
    userId: str
    repoName: str
    branch: str
    provider: Literal["github"]
    hashedResult: str
