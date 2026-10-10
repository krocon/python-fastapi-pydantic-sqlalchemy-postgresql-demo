"""Business logic – knows nothing about HTTP, GraphQL or Protobuf."""

from dataclasses import dataclass, field
from datetime import UTC, datetime

from app.schemas.user import UserCreate, UserUpdate


@dataclass
class User:  # stand-in for the SQLAlchemy model of episode 011
    id: int
    username: str
    email: str
    role: str
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))


_USERS: dict[int, User] = {}  # in-memory until episode 009


def list_users() -> list[User]:
    return list(_USERS.values())


def get_user(user_id: int) -> User | None:
    return _USERS.get(user_id)


def create_user(data: UserCreate) -> User:
    user = User(id=len(_USERS) + 1, **data.model_dump())
    _USERS[user.id] = user
    return user


def update_user(user_id: int, data: UserUpdate) -> User | None:
    user = _USERS.get(user_id)
    if user is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)  # only the fields the client actually sent
    return user
