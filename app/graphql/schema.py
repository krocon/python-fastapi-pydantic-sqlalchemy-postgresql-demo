import strawberry
from sqlalchemy.ext.asyncio import AsyncSession
from strawberry.fastapi import GraphQLRouter

from app.core.database import SessionDep
from app.graphql.types import UserType
from app.services import user_service


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


schema = strawberry.Schema(query=Query)


async def get_context(session: SessionDep) -> dict:
    # same session dependency as REST: one session per request, commit/rollback in get_session
    return {"session": session}


graphql_router = GraphQLRouter(schema, context_getter=get_context)
