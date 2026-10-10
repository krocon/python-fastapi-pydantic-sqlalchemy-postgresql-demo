from typing import Annotated

from fastapi import Query
from pydantic import BaseModel

# reusable, validated query parameters: ?limit=1..100 & offset>=0
Limit = Annotated[int, Query(ge=1, le=100, description="Page size")]
Offset = Annotated[int, Query(ge=0, description="Number of rows to skip")]


class Page[T](BaseModel):
    """One page of results plus the total – generic over the item type."""

    items: list[T]
    total: int
    limit: int
    offset: int
