from fastapi import APIRouter, HTTPException, Request, Response, status
from google.protobuf.message import DecodeError
from pydantic import ValidationError

from app.core.database import SessionDep
from app.models import User
from app.proto import users_pb2
from app.schemas.common import Limit, Offset
from app.schemas.user import UserCreate
from app.services import user_service

PROTOBUF = "application/x-protobuf"

router = APIRouter(prefix="/api/v1/proto", tags=["protobuf"])


class ProtobufResponse(Response):
    media_type = PROTOBUF


def to_proto(user: User, with_items: bool = True) -> users_pb2.User:
    msg = users_pb2.User(id=user.id, username=user.username, email=user.email, role=user.role, is_active=user.is_active)
    if with_items:
        for item in user.items:
            msg.items.add(id=item.id, title=item.title, description=item.description,
                          price=str(item.price), owner_id=item.owner_id)  # Decimal → "19.99"
    return msg


@router.get("/users", response_class=ProtobufResponse)
async def list_users(session: SessionDep, limit: Limit = 20, offset: Offset = 0) -> ProtobufResponse:
    users, total = await user_service.list_users(session, limit=limit, offset=offset, with_items=True)
    body = users_pb2.UserList(users=[to_proto(u) for u in users], total=total)
    return ProtobufResponse(body.SerializeToString())


@router.get("/users/{user_id}", response_class=ProtobufResponse)
async def get_user(user_id: int, session: SessionDep) -> ProtobufResponse:
    user = await user_service.get_user_with_items(session, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return ProtobufResponse(to_proto(user).SerializeToString())


@router.post("/users", status_code=status.HTTP_201_CREATED, response_class=ProtobufResponse)
async def create_user(request: Request, session: SessionDep) -> ProtobufResponse:
    if request.headers.get("content-type") != PROTOBUF:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=f"Use Content-Type: {PROTOBUF}")
    try:
        msg = users_pb2.CreateUserRequest.FromString(await request.body())  # raw bytes in
        data = UserCreate(username=msg.username, email=msg.email, role=msg.role or "user")
    except DecodeError:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail="Invalid protobuf message") from None
    except ValidationError as exc:
        first = exc.errors()[0]  # same Pydantic rules as REST and GraphQL
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, detail=f"{first['loc'][0]}: {first['msg']}") from None
    user = await user_service.create_user(session, data)  # same service as REST and GraphQL
    return ProtobufResponse(to_proto(user, with_items=False).SerializeToString(), status_code=status.HTTP_201_CREATED)
