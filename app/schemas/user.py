from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-z0-9_]+$")
    email: str = Field(max_length=100)
    role: Literal["user", "admin"] = "user"


class UserCreate(UserBase):
    """Request body of POST /api/v1/users."""


class UserRead(UserBase):
    """What the API returns – nothing more, nothing less."""

    model_config = ConfigDict(from_attributes=True)  # read from objects, not only dicts

    id: int
    is_active: bool
    created_at: datetime
