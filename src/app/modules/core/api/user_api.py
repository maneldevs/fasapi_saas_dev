from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import UserCreateCommand, UserFilter, UserResponse
from src.app.modules.core.domain.services.user_service import UserService
from src.app.modules.core.utils.paginator import PageParams, PageParser, PageResponse


router = APIRouter(prefix="/api/core/users", tags=["Core - Users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create(command: UserCreateCommand, service: Annotated[UserService, Depends()]):
    user = service.create(command)
    return user


@router.get("/", response_model=PageResponse[UserResponse])
async def read(
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[UserFilter, Depends()],
    service: Annotated[UserService, Depends()],
):
    users, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(users, UserResponse)
    return parser.generate_page_response(page=page_params.page, size=page_params.size, total=total, content=users)
