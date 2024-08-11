from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import UserCreateCommand, UserResponse
from src.app.modules.core.domain.services.user_service import UserService


router = APIRouter(prefix="/api/core/users", tags=["Core - Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(command: UserCreateCommand, service: Annotated[UserService, Depends()]):
    user = service.create(command)
    return user
