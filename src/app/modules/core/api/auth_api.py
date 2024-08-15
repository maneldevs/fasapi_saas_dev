from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.app.modules.core.domain.models import LoginCommand, LoginResponse
from src.app.modules.core.domain.services.auth_service import AuthService


router = APIRouter(prefix="/api/core/auth", tags=["Core - Auth"])


@router.post("/", response_model=LoginResponse)
async def login(command: Annotated[OAuth2PasswordRequestForm, Depends()], service: Annotated[AuthService, Depends()]):
    login = service.authenticate(LoginCommand.model_validate(command))
    return login
