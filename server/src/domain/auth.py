from pydantic import BaseModel
from datetime import datetime
from typing_extensions import Literal, TypedDict


class CreateMachineTokenInput(TypedDict):
    audience: str
    grant_type: Literal["client_credentials"]
    client_id: str
    client_secret: str


class MachineToken(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]
    expires_at: datetime
