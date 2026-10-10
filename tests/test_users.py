import uuid

from httpx import AsyncClient


def new_user() -> dict:
    name = f"test_{uuid.uuid4().hex[:8]}"  # unique – the database is shared for now (fixed in episode 027)
    return {"username": name, "email": f"{name}@example.com"}


async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


async def test_create_and_read_user(client: AsyncClient) -> None:
    created = await client.post("/api/v1/users", json=new_user())
    assert created.status_code == 201
    user = created.json()
    assert created.headers["location"] == f"/api/v1/users/{user['id']}"

    fetched = await client.get(f"/api/v1/users/{user['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["items"] == []


async def test_invalid_email_is_422(client: AsyncClient) -> None:
    response = await client.post("/api/v1/users", json={"username": "valid_name", "email": "no-mail"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "email"]


async def test_duplicate_is_409(client: AsyncClient) -> None:
    payload = new_user()
    assert (await client.post("/api/v1/users", json=payload)).status_code == 201
    response = await client.post("/api/v1/users", json=payload)
    assert response.status_code == 409
