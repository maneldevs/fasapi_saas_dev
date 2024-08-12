from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.models import GroupSimpleResponse, UserFilter, UserResponse
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.services.user_service import UserService
from src.app.modules.core.utils.paginator import PageParams, PageParser


router = APIRouter(prefix="/core/users")


@router.get("/")
async def user_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[UserFilter, Depends()],
    service: Annotated[UserService, Depends()],
    service_group: Annotated[GroupService, Depends()],
    msg: str = None,
):
    page_params.order_field = "username"
    users, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(users, UserResponse)
    context = parser.generate_web_context(page_params, total, filter, msg)
    groups_in_db = service_group.read_all()
    parser = PageParser(groups_in_db, GroupSimpleResponse)
    groups = parser.parse_list()
    context |= {"groups": groups}
    return main.templates.TemplateResponse(request=request, name="core/user_list.html", context=context)
