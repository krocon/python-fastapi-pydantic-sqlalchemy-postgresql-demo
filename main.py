from fastapi import FastAPI

app = FastAPI(title="Users & Items API")


@app.get("/")
async def root() -> dict[str, str]:
    return {"status": "online"}
