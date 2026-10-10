"""Tests run against a real PostgreSQL: own database, migrated by Alembic, every test rolled back."""

import asyncio
from collections.abc import AsyncIterator

import pytest
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy import make_url, text
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.core.config import settings
from app.core.database import get_session
from app.main import app

TEST_URL = make_url(str(settings.database_url)).set(database="app_test")


@pytest.fixture(scope="session")
async def engine() -> AsyncIterator[AsyncEngine]:
    # 1. create the test database once (CREATE DATABASE needs autocommit)
    admin = create_async_engine(TEST_URL.set(database="postgres"), isolation_level="AUTOCOMMIT")
    async with admin.connect() as conn:
        await conn.execute(text("DROP DATABASE IF EXISTS app_test WITH (FORCE)"))
        await conn.execute(text("CREATE DATABASE app_test"))
    await admin.dispose()

    # 2. build the schema with the real migrations – so the migrations are tested, too
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", TEST_URL.render_as_string(hide_password=False))
    await asyncio.to_thread(command.upgrade, cfg, "head")

    engine = create_async_engine(TEST_URL)
    yield engine
    await engine.dispose()


@pytest.fixture
async def session(engine: AsyncEngine) -> AsyncIterator[AsyncSession]:
    # 3. one outer transaction per test – rolled back at the end, the database stays empty
    async with engine.connect() as conn:
        outer = await conn.begin()
        session = AsyncSession(bind=conn, expire_on_commit=False, join_transaction_mode="create_savepoint")
        yield session
        await session.close()
        await outer.rollback()


@pytest.fixture
async def client(session: AsyncSession) -> AsyncIterator[AsyncClient]:
    async def test_session() -> AsyncIterator[AsyncSession]:
        try:
            yield session
            await session.commit()  # only releases a SAVEPOINT
        except Exception:
            await session.rollback()  # back to the SAVEPOINT
            raise

    app.dependency_overrides[get_session] = test_session  # REST, GraphQL and Protobuf use it
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
