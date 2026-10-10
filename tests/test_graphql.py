from httpx import AsyncClient


async def gql(client: AsyncClient, query: str) -> dict:
    response = await client.post("/graphql", json={"query": query})
    assert response.status_code == 200
    return response.json()


async def test_mutation_and_nested_query(client: AsyncClient) -> None:
    created = await gql(client, 'mutation { createUser(input: {username: "carol", email: "carol@example.com"}) { id } }')
    user_id = created["data"]["createUser"]["id"]
    await gql(client, f'mutation {{ createItem(input: {{title: "Headset", price: "79.00", ownerId: {user_id}}}) {{ id }} }}')

    result = await gql(client, "{ users { username items { title price } } }")
    assert result["data"]["users"] == [{"username": "carol", "items": [{"title": "Headset", "price": "79.00"}]}]


async def test_same_validation_as_rest(client: AsyncClient) -> None:
    result = await gql(client, 'mutation { createUser(input: {username: "root", email: "x@example.com"}) { id } }')
    assert result["errors"][0]["extensions"]["code"] == "BAD_USER_INPUT"
