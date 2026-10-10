from typing import Literal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Body of POST /api/v1/users – everything else is rejected with 422."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-z0-9_]+$")
    email: str = Field(max_length=100)
    role: Literal["user", "admin"] = "user"
