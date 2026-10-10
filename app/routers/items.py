from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.schemas.item import ItemCreate, ItemRead
from app.services import item_service, user_service

router = APIRouter(prefix="/api/v1/items", tags=["items"])


@router.get("")
async def list_items(session: SessionDep) -> list[ItemRead]:
    return await item_service.list_items(session)


@router.post("", status_code=201)
async def create_item(payload: ItemCreate, session: SessionDep) -> ItemRead:
    if await user_service.get_user(session, payload.owner_id) is None:
        raise HTTPException(status_code=404, detail="Owner not found")
    return await item_service.create_item(session, payload)
