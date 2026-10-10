from httpx import AsyncClient

from app.proto import users_pb2

PROTOBUF = {"Content-Type": "application/x-protobuf"}


async def test_create_and_list_binary(client: AsyncClient) -> None:
    request = users_pb2.CreateUserRequest(username="dave", email="dave@example.com")
    created = await client.post("/api/v1/proto/users", content=request.SerializeToString(), headers=PROTOBUF)
    assert created.status_code == 201
    assert created.headers["content-type"] == "application/x-protobuf"
    assert users_pb2.User.FromString(created.content).username == "dave"

    listed = users_pb2.UserList.FromString((await client.get("/api/v1/proto/users")).content)
    assert listed.total == 1


async def test_json_is_rejected_with_415(client: AsyncClient) -> None:
    response = await client.post("/api/v1/proto/users", json={"username": "dave"})
    assert response.status_code == 415
