from fastapi import FastAPI

from app.routers import users

app = FastAPI(title="Users & Items API", version="0.3.0")
app.include_router(users.router)


@app.get("/", tags=["status"])
async def root() -> dict[str, str]:
    return {"status": "online"}
