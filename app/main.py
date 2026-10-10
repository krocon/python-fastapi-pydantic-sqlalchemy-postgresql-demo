import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import engine
from app.core.errors import register_error_handlers
from app.graphql.schema import graphql_router
from app.routers import health, items, proto, users

logging.basicConfig(level=logging.INFO, format="%(levelname)s:     %(name)s – %(message)s")
logger = logging.getLogger("app")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # before yield: runs once at startup, before the first request
    logger.info("starting %s %s", settings.app_name, app.version)
    yield
    # after yield: runs once at shutdown – close all pooled connections cleanly
    await engine.dispose()
    logger.info("database pool closed")


app = FastAPI(title=settings.app_name, version="1.0.0", debug=settings.debug, lifespan=lifespan)
register_error_handlers(app)
app.include_router(health.router)
app.include_router(users.router)
app.include_router(items.router)
app.include_router(proto.router)
app.include_router(graphql_router, prefix="/graphql", tags=["graphql"])  # GraphiQL in the browser


@app.get("/", tags=["status"])
async def root() -> dict[str, str]:
    return {"status": "online", "app": settings.app_name}
