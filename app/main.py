from fastapi import FastAPI

from app.core.config import settings
from app.core.errors import register_error_handlers
from app.graphql.schema import graphql_router
from app.routers import items, users

app = FastAPI(title=settings.app_name, version="0.22.0", debug=settings.debug)
register_error_handlers(app)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])  # GraphiQL in the browser


@app.get("/", tags=["status"])
async def root() -> dict[str, str]:
    return {"status": "online", "app": settings.app_name}
