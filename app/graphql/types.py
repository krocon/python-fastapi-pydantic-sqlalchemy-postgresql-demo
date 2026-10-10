from decimal import Decimal
from typing import Self

import strawberry

from app.models import Item, User


@strawberry.type
class ItemType:
    id: int
    title: str
    description: str
    price: Decimal
    owner_id: int

    @classmethod
    def from_model(cls, item: Item) -> Self:
        return cls(id=item.id, title=item.title, description=item.description, price=item.price, owner_id=item.owner_id)


@strawberry.type
class UserType:
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    items: list[ItemType]

    @classmethod
    def from_model(cls, user: User) -> Self:
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            items=[ItemType.from_model(i) for i in user.items],
        )
