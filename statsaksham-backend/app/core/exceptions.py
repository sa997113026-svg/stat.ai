from typing import Any, List, Optional
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        details: Optional[List[Any]] = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []
        super().__init__(message)


async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
    req_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=exc.status_code,
        headers={"X-Request-ID": req_id},
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            },
            "request_id": req_id,
        },
    )


async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    req_id = getattr(request.state, "request_id", "unknown")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        headers={"X-Request-ID": req_id},
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": exc.errors(),
            },
            "request_id": req_id,
        },
    )
