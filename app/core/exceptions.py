from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logger = logging.getLogger("closira")


class ClosiraException(Exception):
    """Base exception for all domain-specific errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code


class NotFoundError(ClosiraException):
    def __init__(self, item_name: str, item_id: str | int):
        super().__init__(f"{item_name} with id {item_id} not found", status_code=404)


async def custom_exception_handler(request: Request, exc: ClosiraException):
    logger.warning(
        "Domain exception occurred",
        extra={
            "path": request.url.path,
            "error": exc.message,
            "status_code": exc.status_code,
        },
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "Validation error", extra={"path": request.url.path, "errors": exc.errors()}
    )
    return JSONResponse(
        status_code=422,
        content={"detail": "Validation error", "errors": exc.errors()},
    )
