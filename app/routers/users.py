from fastapi import APIRouter, HTTPException

from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("")
async def list_users() -> list[UserRead]:
    return user_service.list_users()


@router.get("/{user_id}")
async def get_user(user_id: int) -> UserRead:
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("", status_code=201)
async def create_user(payload: UserCreate) -> UserRead:
    return user_service.create_user(payload)


@router.patch("/{user_id}")
async def update_user(user_id: int, payload: UserUpdate) -> UserRead:
    user = user_service.update_user(user_id, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
