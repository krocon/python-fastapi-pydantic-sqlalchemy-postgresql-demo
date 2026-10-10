import asyncio

from fastapi import APIRouter, Response, status
from sqlalchemy import text

from app.core.database import SessionDep

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def live() -> dict[str, str]:
    """Liveness: the process answers. Never touches the database."""
    return {"status": "ok"}


@router.get("/ready", responses={status.HTTP_503_SERVICE_UNAVAILABLE: {"description": "Database not reachable"}})
async def ready(session: SessionDep, response: Response) -> dict[str, str]:
    """Readiness: may this instance receive traffic? Only if PostgreSQL answers within 2 seconds."""
    try:
        async with asyncio.timeout(2):
            await session.execute(text("SELECT 1"))
    except Exception:  # connection refused, timeout, auth error …
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return {"status": "unavailable", "database": "down"}
    return {"status": "ok", "database": "up"}
