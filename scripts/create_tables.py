"""uv run python -m scripts.create_tables – temporary until Alembic (episode 018)."""

import asyncio

from app.core.database import engine
from app.models import Base


async def main() -> None:
    engine.echo = True  # show the generated DDL
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await engine.dispose()


asyncio.run(main())
