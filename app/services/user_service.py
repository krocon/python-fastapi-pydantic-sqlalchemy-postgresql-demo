"""Business logic – knows nothing about HTTP, GraphQL or Protobuf."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserCreate, UserUpdate


async def list_users(session: AsyncSession, q: str | None = None, active: bool | None = None) -> Sequence[User]:
    stmt = select(User).order_by(User.id)
    if q:
        stmt = stmt.where(User.username.ilike(f"%{q}%"))  # bound parameter – no SQL injection
    if active is not None:
        stmt = stmt.where(User.is_active == active)
    return (await session.scalars(stmt)).all()


async def get_by_username(session: AsyncSession, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return (await session.execute(stmt)).scalar_one_or_none()


async def get_user(session: AsyncSession, user_id: int) -> User | None:
    return await session.get(User, user_id)


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User(**data.model_dump())
    session.add(user)
    await session.flush()  # INSERT now → id is set (details: episode 016)
    await session.refresh(user)  # load server defaults like created_at
    return user


async def update_user(session: AsyncSession, user_id: int, data: UserUpdate) -> User | None:
    user = await session.get(User, user_id)
    if user is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)  # only the fields the client actually sent
    return user  # commit happens in get_session
