"""Business logic – knows nothing about HTTP, GraphQL or Protobuf."""

from app.schemas.user import UserCreate

_USERS: dict[int, dict] = {}  # in-memory until episode 009


def list_users() -> list[dict]:
    return list(_USERS.values())


def get_user(user_id: int) -> dict | None:
    return _USERS.get(user_id)


def create_user(data: UserCreate) -> dict:
    user = {"id": len(_USERS) + 1, **data.model_dump()}
    _USERS[user["id"]] = user
    return user
