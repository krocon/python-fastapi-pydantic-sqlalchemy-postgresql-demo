from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas.item import ItemCreate


async def list_items(session: AsyncSession) -> Sequence[Item]:
    return (await session.scalars(select(Item).order_by(Item.id))).all()


async def create_item(session: AsyncSession, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    session.add(item)
    await session.flush()
    return item
