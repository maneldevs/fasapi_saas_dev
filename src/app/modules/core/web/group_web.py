from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.group_service import GroupService
from src.app.modules.core.domain.models import GroupFilter
from src.app.modules.core.utils.paginator import PageParams, PageResponse

router = APIRouter(prefix="/core/groups")


@router.get("/")
async def form(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[GroupFilter, Depends()],
    service: Annotated[GroupService, Depends()],
):
    groups, total = service.read_all_paginated(page_params, filter)
    page = PageResponse(page=page_params.page, size=page_params.size, total=total, content=groups)
    context = page.model_dump()
    context |= filter.model_dump()
    context |= {"query_params": f"&size={page_params.size}&order_field={page_params.order_field}" +
                f"&direction={page_params.direction.value}&target={filter.target if filter.target else ''}"}
    return main.templates.TemplateResponse(request=request, name="core/group_list.html", context=context)
