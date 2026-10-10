from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

# one engine per process = one connection pool
engine = create_async_engine(
    str(settings.database_url),  # postgresql+asyncpg://…  → async driver
    pool_size=5,
    pool_pre_ping=True,  # detect dead connections before using them
    echo=settings.debug,  # log SQL in debug mode
)

# factory for AsyncSession objects – one session per unit of work
SessionFactory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncIterator[AsyncSession]:
    """One session per request: commit if the endpoint succeeds, roll back if it raises."""
    async with SessionFactory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise


# scope="function": commit BEFORE the response is sent – a failing commit becomes an error response
SessionDep = Annotated[AsyncSession, Depends(get_session, scope="function")]
