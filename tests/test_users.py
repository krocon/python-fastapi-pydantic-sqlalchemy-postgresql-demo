from httpx import AsyncClient

ALICE = {"username": "alice", "email": "alice@example.com"}


async def test_root(client: AsyncClient) -> None:
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


async def test_every_test_starts_empty(client: AsyncClient) -> None:
    response = await client.get("/api/v1/users")
    assert response.json()["total"] == 0


async def test_create_and_read_user(client: AsyncClient) -> None:
    created = await client.post("/api/v1/users", json=ALICE)  # same name in every test – no clashes
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


async def test_duplicate_is_409_and_session_survives(client: AsyncClient) -> None:
    assert (await client.post("/api/v1/users", json=ALICE)).status_code == 201
    duplicate = await client.post("/api/v1/users", json={**ALICE, "email": "other@example.com"})
    assert duplicate.status_code == 409
    assert duplicate.json() == {"detail": "Username already exists"}
    assert (await client.get("/api/v1/users")).json()["total"] == 1


async def test_patch_only_changes_sent_fields(client: AsyncClient) -> None:
    user = (await client.post("/api/v1/users", json=ALICE)).json()
    patched = (await client.patch(f"/api/v1/users/{user['id']}", json={"role": "admin"})).json()
    assert patched["role"] == "admin"
    assert patched["email"] == ALICE["email"]
    assert patched["updated_at"] is not None


async def test_delete_cascades_items(client: AsyncClient) -> None:
    user = (await client.post("/api/v1/users", json=ALICE)).json()
    await client.post("/api/v1/items", json={"title": "Keyboard", "price": "49.90", "owner_id": user["id"]})
    assert (await client.delete(f"/api/v1/users/{user['id']}")).status_code == 204
    assert (await client.get("/api/v1/items")).json()["total"] == 0
