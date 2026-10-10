from fastapi import APIRouter, HTTPException

from app.core.database import SessionDep
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("")
async def list_users(session: SessionDep) -> list[UserRead]:
    return await user_service.list_users(session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep) -> UserRead:
    user = await user_service.get_user(session, user_id)
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
