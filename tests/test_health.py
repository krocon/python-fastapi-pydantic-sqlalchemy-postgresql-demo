from httpx import AsyncClient


async def test_live(client: AsyncClient) -> None:
    assert (await client.get("/health/live")).json() == {"status": "ok"}


async def test_ready_checks_the_database(client: AsyncClient) -> None:
    response = await client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "up"}
