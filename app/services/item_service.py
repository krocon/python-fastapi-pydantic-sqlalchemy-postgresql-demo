from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas.item import ItemCreate


async def list_items(session: AsyncSession) -> Sequence[Item]:
    return (await session.scalars(select(Item).order_by(Item.id))).all()


async def list_items_of_owner(session: AsyncSession, owner_id: int) -> Sequence[Item]:
    stmt = select(Item).where(Item.owner_id == owner_id).order_by(Item.price.desc())
    return (await session.scalars(stmt)).all()


async def create_item(session: AsyncSession, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    session.add(item)
    await session.flush()
    return item
