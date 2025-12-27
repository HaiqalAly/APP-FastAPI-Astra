from fastapi import Request
from fastapi.responses import JSONResponse


async def user_already_exists_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


async def invalid_credentials_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=401,
        content={"detail": str(exc)},
        headers={"WWW-Authenticate": "Bearer"},
    )


async def inactive_user_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def insufficient_permissions_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=403, content={"detail": str(exc)})


async def token_expired_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


async def invalid_token_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


async def invalid_password_confirmation_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=401, content={"detail": str(exc)})


async def invalid_confirmation_text_handler(request: Request, exc: Exception):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
