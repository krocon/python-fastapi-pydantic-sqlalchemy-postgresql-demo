from fastapi import FastAPI, HTTPException

app = FastAPI(title="Users & Items API", version="0.2.0")

USERS = {1: "alice", 2: "bob"}  # in-memory for now – the database comes in episode 009


@app.get("/", tags=["status"])
async def root() -> dict[str, str]:
    return {"status": "online"}


@app.get("/users/{user_id}", tags=["users"], summary="Get one user")
async def get_user(user_id: int) -> dict[str, int | str]:
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user_id, "username": USERS[user_id]}
