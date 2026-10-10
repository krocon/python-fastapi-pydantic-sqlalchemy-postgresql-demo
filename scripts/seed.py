"""uv run python -m scripts.seed – one user with two items, saved in one go."""

import asyncio
from decimal import Decimal

from app.core.database import SessionFactory, engine
from app.models import Item, User


async def main() -> None:
    async with SessionFactory() as session:
        alice = User(username="alice", email="alice@example.com")
        alice.items = [
            Item(title="Keyboard", price=Decimal("49.90")),
            Item(title="Mouse", price=Decimal("19.99")),
        ]
        session.add(alice)  # the items come along (cascade)
        await session.commit()
        print(f"user {alice.id}: {[(i.id, i.title, i.owner_id) for i in alice.items]}")
    await engine.dispose()


asyncio.run(main())
