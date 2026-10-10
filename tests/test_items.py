from decimal import Decimal

from httpx import AsyncClient


async def test_price_is_exact_decimal(client: AsyncClient) -> None:
    owner = (await client.post("/api/v1/users", json={"username": "bob", "email": "bob@example.com"})).json()
    for _ in range(10):
        await client.post("/api/v1/items", json={"title": "Mouse", "price": "19.99", "owner_id": owner["id"]})
    items = (await client.get("/api/v1/items")).json()["items"]
    assert items[0]["price"] == "19.99"  # Decimal → JSON string, no float noise
    assert sum(float(i["price"]) for i in items) != 199.90  # float: 199.89999999999998
    assert sum(Decimal(i["price"]) for i in items) == Decimal("199.90")


async def test_unknown_owner_is_404(client: AsyncClient) -> None:
    response = await client.post("/api/v1/items", json={"title": "Ghost", "price": "1.00", "owner_id": 999})
    assert response.status_code == 404


async def test_pagination_limit_is_validated(client: AsyncClient) -> None:
    assert (await client.get("/api/v1/items?limit=1000")).status_code == 422
