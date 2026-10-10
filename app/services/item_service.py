from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Item
from app.schemas.item import ItemCreate


async def list_items(session: AsyncSession, limit: int = 20, offset: int = 0) -> tuple[Sequence[Item], int]:
    total = await session.scalar(select(func.count()).select_from(Item))
    page = await session.scalars(select(Item).order_by(Item.id).limit(limit).offset(offset))
    return page.all(), total or 0


async def list_items_of_owner(session: AsyncSession, owner_id: int) -> Sequence[Item]:
    stmt = select(Item).where(Item.owner_id == owner_id).order_by(Item.price.desc())
    return (await session.scalars(stmt)).all()


async def create_item(session: AsyncSession, data: ItemCreate) -> Item:
    item = Item(**data.model_dump())
    session.add(item)
    await session.flush()
    return item
