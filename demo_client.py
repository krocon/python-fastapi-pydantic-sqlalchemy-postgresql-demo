"""uv run python demo_client.py – one user, three APIs, one database.

Creates a user via REST, adds an item via GraphQL and reads everything back via Protobuf.
Needs a running API (uv run fastapi dev  or  docker compose up).
"""

import uuid

import httpx

from app.proto import users_pb2

BASE = "http://localhost:8000"


def main() -> None:
    name = f"demo_{uuid.uuid4().hex[:6]}"
    with httpx.Client(base_url=BASE) as http:
        # 1. REST: JSON in, JSON out
        rest = http.post("/api/v1/users", json={"username": name, "email": f"{name}@example.com"})
        user = rest.json()
        print(f"REST     POST /api/v1/users      → {rest.status_code}, id={user['id']}, {len(rest.content)} bytes")

        # 2. GraphQL: one endpoint, the client picks the fields
        mutation = f'mutation {{ createItem(input: {{title: "Keyboard", price: "49.90", ownerId: {user["id"]}}}) {{ id price }} }}'
        gql = http.post("/graphql", json={"query": mutation})
        item = gql.json()["data"]["createItem"]
        print(f"GraphQL  createItem               → {gql.status_code}, item={item['id']}, price={item['price']}")

        # 3. Protobuf: binary in, binary out
        proto = http.get(f"/api/v1/proto/users/{user['id']}")
        message = users_pb2.User.FromString(proto.content)
        print(f"Protobuf GET /api/v1/proto/users/{user['id']} → {proto.status_code}, "
              f"{message.username} has {len(message.items)} item(s), {len(proto.content)} bytes")

        # same user, same item – three protocols, one service layer, one PostgreSQL
        same = http.get(f"/api/v1/users/{user['id']}").json()
        print(f"REST     GET  /api/v1/users/{user['id']}     → {len(same['items'])} item(s), price {same['items'][0]['price']}")


if __name__ == "__main__":
    main()
