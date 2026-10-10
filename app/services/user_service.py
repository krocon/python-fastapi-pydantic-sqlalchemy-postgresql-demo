"""Business logic – knows nothing about HTTP, GraphQL or Protobuf."""

from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.schemas.user import UserCreate, UserUpdate


async def list_users(session: AsyncSession) -> Sequence[User]:
    return (await session.scalars(select(User).order_by(User.id))).all()


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
