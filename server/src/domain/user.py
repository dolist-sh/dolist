""" 
This module contains the Pydantic models that define the core data structure (input, output, core models).
"""
from uuid import UUID
from typing import List
from typing_extensions import Literal, TypedDict
from pydantic import BaseModel


class OAuth(TypedDict):
    type: Literal["github"]
    token: str # TODO: Token need to be encrypted


class User(BaseModel):
    id: UUID  # uuid v4
    type: Literal["admin"]
    email: str  # unique value
    name: str
    profileUrl: str
    oauth: List[OAuth]
    createdAt: int  # Unix timestamp
