from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.models import UserFilter, UserResponse
from src.app.modules.core.domain.services.user_service import UserService
from src.app.modules.core.utils.paginator import PageParams, PageParser


router = APIRouter(prefix="/core/users")


@router.get("/")
async def user_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[UserFilter, Depends()],
    service: Annotated[UserService, Depends()],
    msg: str = None,
):
    page_params.order_field = "username"
    users, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(users, UserResponse)
    context = parser.generate_web_context(page_params, total, filter, msg)
    return main.templates.TemplateResponse(request=request, name="core/user_list.html", context=context)
