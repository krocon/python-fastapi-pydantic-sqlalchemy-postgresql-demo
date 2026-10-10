from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

# constraint names come from the naming convention in app/models/base.py
CONFLICT_MESSAGES = {
    "uq_users_username": "Username already exists",
    "uq_users_email": "Email already exists",
}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
        # the UNIQUE constraint in PostgreSQL is the single source of truth – no racy "SELECT first"
        constraint = getattr(exc.orig.__cause__, "constraint_name", None)
        detail = CONFLICT_MESSAGES.get(constraint, "Conflict with existing data")
        return JSONResponse(status_code=status.HTTP_409_CONFLICT, content={"detail": detail})
