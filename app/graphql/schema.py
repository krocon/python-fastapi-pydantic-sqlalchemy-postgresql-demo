import dataclasses

import strawberry
from graphql import GraphQLError
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from app.core.database import SessionDep
from app.core.errors import CONFLICT_MESSAGES
from app.graphql.types import CreateItemInput, CreateUserInput, ItemType, UserType
from app.schemas.item import ItemCreate
from app.schemas.user import UserCreate
from app.services import item_service, user_service


@strawberry.type
class Query:
    @strawberry.field(description="Users with their items – the client picks the fields")
    async def users(self, info: strawberry.Info, limit: int = 20, offset: int = 0) -> list[UserType]:
        session: AsyncSession = info.context["session"]
        users, _ = await user_service.list_users(session, limit=min(limit, 100), offset=offset, with_items=True)
        return [UserType.from_model(u) for u in users]

    @strawberry.field(description="One user by id")
    async def user(self, info: strawberry.Info, id: int) -> UserType | None:
        user = await user_service.get_user_with_items(info.context["session"], id)
        return UserType.from_model(user) if user else None


def validated[M](model: type[M], data: object) -> M:
    """Same Pydantic rules as REST – one source of truth for validation."""
    try:
        return model.model_validate(dataclasses.asdict(data))
    except ValidationError as exc:
        first = exc.errors()[0]
        raise GraphQLError(f"{first['loc'][0]}: {first['msg']}", extensions={"code": "BAD_USER_INPUT"}) from None


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Create a user – validated by the same Pydantic model as REST")
    async def create_user(self, info: strawberry.Info, input: CreateUserInput) -> UserType:
        session: AsyncSession = info.context["session"]
        data = validated(UserCreate, input)
        try:
            user = await user_service.create_user(session, data)
        except IntegrityError as exc:
            await session.rollback()
            constraint = getattr(exc.orig.__cause__, "constraint_name", None)
            raise GraphQLError(CONFLICT_MESSAGES.get(constraint, "Conflict"), extensions={"code": "CONFLICT"}) from None
        return UserType(id=user.id, username=user.username, email=user.email, role=user.role,
                        is_active=user.is_active, items=[])

    @strawberry.mutation(description="Create an item for an existing user")
    async def create_item(self, info: strawberry.Info, input: CreateItemInput) -> ItemType:
        session: AsyncSession = info.context["session"]
        data = validated(ItemCreate, input)
        if await user_service.get_user(session, data.owner_id) is None:
            raise GraphQLError("Owner not found", extensions={"code": "NOT_FOUND"})
        return ItemType.from_model(await item_service.create_item(session, data))


schema = strawberry.Schema(query=Query, mutation=Mutation)


async def get_context(session: SessionDep) -> dict:
    # same session dependency as REST: one session per request, commit/rollback in get_session
    return {"session": session}


graphql_router = GraphQLRouter(schema, context_getter=get_context)
