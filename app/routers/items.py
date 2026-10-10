from fastapi import APIRouter, HTTPException, status

from app.core.database import SessionDep
from app.schemas.common import Limit, Offset, Page
from app.schemas.item import ItemCreate, ItemRead
from app.services import item_service, user_service

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.get("")
async def list_items(session: SessionDep, limit: Limit = 20, offset: Offset = 0) -> Page[ItemRead]:
    items, total = await item_service.list_items(session, limit=limit, offset=offset)
    return Page[ItemRead](items=items, total=total, limit=limit, offset=offset)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_item(payload: ItemCreate, session: SessionDep) -> ItemRead:
    if await user_service.get_user(session, payload.owner_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    return await item_service.create_item(session, payload)
