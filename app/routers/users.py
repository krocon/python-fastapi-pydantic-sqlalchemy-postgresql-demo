from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.schemas.item import ItemRead
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithItems
from app.services import item_service, user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("")
async def list_users(session: SessionDep, q: str | None = None, active: bool | None = None) -> list[UserRead]:
    return await user_service.list_users(session, q=q, active=active)


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep) -> UserWithItems:
    user = await user_service.get_user_with_items(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", status_code=201)
async def create_user(payload: UserCreate, session: SessionDep) -> UserRead:
    return await user_service.create_user(session, payload)


@router.patch("/{user_id}")
async def update_user(user_id: int, payload: UserUpdate, session: SessionDep) -> UserRead:
    user = await user_service.update_user(session, user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/{user_id}/items")
async def list_user_items(user_id: int, session: SessionDep) -> list[ItemRead]:
    if await user_service.get_user(session, user_id) is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await item_service.list_items_of_owner(session, user_id)
