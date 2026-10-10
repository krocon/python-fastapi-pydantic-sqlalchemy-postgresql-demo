"""Business logic – knows nothing about HTTP, GraphQL or Protobuf."""

_USERS: dict[int, str] = {1: "alice", 2: "bob"}  # in-memory until episode 009


def list_users() -> list[dict[str, int | str]]:
    return [{"id": uid, "username": name} for uid, name in _USERS.items()]


def get_user(user_id: int) -> dict[str, int | str] | None:
    name = _USERS.get(user_id)
    return None if name is None else {"id": user_id, "username": name}
