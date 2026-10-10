from fastapi import APIRouter, HTTPException, Response, status

from app.core.database import SessionDep
from app.schemas.item import ItemRead
from app.schemas.user import UserCreate, UserRead, UserUpdate, UserWithItems
from app.services import item_service, user_service

router = APIRouter(prefix="/api/v1/users", tags=["users"])

NOT_FOUND = {status.HTTP_404_NOT_FOUND: {"description": "User not found"}}
CONFLICT = {status.HTTP_409_CONFLICT: {"description": "Username or email already exists"}}


def user_not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("")
async def list_users(session: SessionDep, q: str | None = None, active: bool | None = None) -> list[UserRead]:
    return await user_service.list_users(session, q=q, active=active)


@router.get("/{user_id}", responses=NOT_FOUND)
async def get_user(user_id: int, session: SessionDep) -> UserWithItems:
    user = await user_service.get_user_with_items(session, user_id)
    if user is None:
        raise user_not_found()
    return user


@router.post("", status_code=status.HTTP_201_CREATED, responses=CONFLICT)
async def create_user(payload: UserCreate, session: SessionDep, response: Response) -> UserRead:
    user = await user_service.create_user(session, payload)
    response.headers["Location"] = f"{router.prefix}/{user.id}"  # where the new resource lives
    return user


@router.patch("/{user_id}", responses=NOT_FOUND | CONFLICT)
async def update_user(user_id: int, payload: UserUpdate, session: SessionDep) -> UserRead:
    user = await user_service.update_user(session, user_id, payload)
    if user is None:
        raise user_not_found()
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, responses=NOT_FOUND)
async def delete_user(user_id: int, session: SessionDep) -> None:
    if not await user_service.delete_user(session, user_id):
        raise user_not_found()


@router.get("/{user_id}/items", responses=NOT_FOUND)
async def list_user_items(user_id: int, session: SessionDep) -> list[ItemRead]:
    if await user_service.get_user(session, user_id) is None:
        raise user_not_found()
    return await item_service.list_items_of_owner(session, user_id)
