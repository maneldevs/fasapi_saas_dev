from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.app.configuration.exceptions import BaseError


async def base_handler(request: Request, exc: BaseError):
    detail = {
        "args": exc.original_exception.args,
        "input": await request.json(),
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={"type": exc.type, "msg": exc.msg, "status": exc.status_code, "detail": detail},
    )


async def validation_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"type": "validation", "msg": "validation error", "status": 422, "detail": exc.errors()},
    )
