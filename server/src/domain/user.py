""" 
This module contains the Pydantic models that define the core data structure (input, output, core models).
"""
from uuid import UUID
from typing_extensions import Literal
from pydantic import BaseModel


class User(BaseModel):
    id: UUID  # uuid v4
    email: str # unique value
    type: Literal["admin"]
    connected: Literal[Literal["github", "gitlab"]]
    createdAt: int  # TODO: Find the right type definition for Unix timestamp
