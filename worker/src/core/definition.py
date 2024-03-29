# import datetime
from typing_extensions import TypedDict, Literal


class MachineToken(TypedDict):
    access_token: str
    token_type: Literal["Bearer"]
    expires_at: str


class ParseRequestMsg(TypedDict):
    userId: str
    token: str
    mrepoId: str
    repoName: str
    branch: str
    provider: Literal["github"]
