from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

RESERVED_NAMES = {"admin", "root", "api"}


class UserBase(BaseModel):
    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-z0-9_]+$")
    email: EmailStr = Field(max_length=100)
    role: Literal["user", "admin"] = "user"


class UserCreate(UserBase):
    """Request body of POST /api/v1/users."""

    @field_validator("username", mode="before")
    @classmethod
    def normalize_username(cls, value: object) -> object:
        # runs BEFORE the type and pattern checks: "  Alice " → "alice"
        return value.strip().lower() if isinstance(value, str) else value

    @field_validator("username")
    @classmethod
    def not_reserved(cls, value: str) -> str:
        if value in RESERVED_NAMES:
            raise ValueError(f"'{value}' is reserved")
        return value


class UserRead(UserBase):
    """What the API returns – nothing more, nothing less."""

    model_config = ConfigDict(from_attributes=True)  # read from objects, not only dicts

    id: int
    is_active: bool
    created_at: datetime
