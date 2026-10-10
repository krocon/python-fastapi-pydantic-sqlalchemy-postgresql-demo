from fastapi import FastAPI

from app.core.config import settings
from app.routers import items, users

app = FastAPI(title=settings.app_name, version="0.14.0", debug=settings.debug)
app.include_router(users.router)
app.include_router(items.router)


@app.get("/", tags=["status"])
async def root() -> dict[str, str]:
    return {"status": "online", "app": settings.app_name}
