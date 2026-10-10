from fastapi import APIRouter, HTTPException

from app.services import user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])


@router.get("")
async def list_users() -> list[dict[str, int | str]]:
    return user_service.list_users()


@router.get("/{user_id}")
async def get_user(user_id: int) -> dict[str, int | str]:
    user = user_service.get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
