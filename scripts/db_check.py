"""uv run python -m scripts.db_check – is PostgreSQL reachable?"""

import asyncio

from sqlalchemy import text

from app.core.database import SessionFactory, engine


async def main() -> None:
    async with SessionFactory() as session:
        version = await session.scalar(text("select version()"))
        print(version)
    await engine.dispose()


asyncio.run(main())
