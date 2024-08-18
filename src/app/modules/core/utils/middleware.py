from fastapi import Request
from src.app.configuration.settings import settings
from src.app.modules.core.utils import crypto


class AddUsernameMiddleware:

    async def __call__(self, request: Request, call_next: callable):
        username = None
        try:
            token = request.cookies["token"]
            payload: dict = crypto.decode_token(token, settings.secret_key, settings.algorithm)
            username = payload.get("sub")
        except Exception:
            pass
        request.state.principal_username = username
        response = await call_next(request)
        return response
