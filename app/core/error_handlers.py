import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from app.core.exceptions import AppException
from app.core.responses import ErrorResponse


def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(message=exc.message).model_dump(),
    )


def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    errors = [
        f"{'.'.join(str(l) for l in e['loc'])}: {e['msg']}" for e in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            message="Validation error.", detail=errors
        ).model_dump(),
    )


def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    return JSONResponse(
        status_code=409,
        content=ErrorResponse(
            message="Database integrity error.", detail=str(exc.orig)
        ).model_dump(),
    )


def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.exception("[500] Unhandled exception on %s %s", request.method, request.url)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(message="Internal server error.").model_dump(),
    )
