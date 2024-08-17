from typing import Annotated
from fastapi import Depends, Cookie, Header
from fastapi.security import OAuth2PasswordBearer

from src.app.configuration.settings import settings
from src.app.configuration.exceptions import ForbiddenError, TokenInvalidError
from src.app.modules.core.domain.models import User
from src.app.modules.core.persistence.user_repo import UserRepo
from src.app.modules.core.utils import crypto


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def token_bearer(authorization: Annotated[str | None, Header()] = None) -> str | None:
    return authorization.replace("Bearer ", "") if authorization else None


def token_cookie(token: Annotated[str | None, Cookie()] = None) -> str | None:
    return token


def token(
    token_bearer: Annotated[str | None, Depends(token_bearer)],
    token_cookie: Annotated[str | None, Depends(token_cookie)],
) -> str | None:
    return token_bearer if token_bearer else token_cookie


Token = Annotated[str | None, Depends(token)]


def principal(user_repo: Annotated[UserRepo, Depends()], token: Token):
    if token is None:
        raise TokenInvalidError
    principal: User | None = None
    payload: dict = crypto.decode_token(token, settings.secret_key, settings.algorithm)
    username: str | None = payload.get("sub")
    if username:
        principal = user_repo.read_by_username(username)
    if principal is None or not principal.active:
        raise TokenInvalidError
    return principal


Principal = Annotated[User, Depends(principal)]


def principal_god(principal: Principal):
    if not principal or not principal.is_god:
        raise ForbiddenError
    return principal


Principal_god = Annotated[User, Depends(principal_god)]
