from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.api.v1.router import api_router
from app.core.error_handlers import (
    app_exception_handler,
    generic_exception_handler,
    integrity_error_handler,
    validation_exception_handler,
)
from app.core.exceptions import AppException

def create_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI Starter",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # ── Exception handlers ───────────────────────────────────────────────────
    app.add_exception_handler(AppException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # ── Routers ──────────────────────────────────────────────────────────────
    app.include_router(api_router)

    @app.get("/health", tags=["Health"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
