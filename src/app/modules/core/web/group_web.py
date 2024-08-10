from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from src.app import main
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import GroupCreateCommand, GroupFilter
from src.app.modules.core.utils.paginator import PageParams, PageResponse
from src.app.modules.core.domain.forms import GroupCreateForm

router = APIRouter(prefix="/core/groups")


@router.get("/")
async def group_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[GroupFilter, Depends()],
    service: Annotated[GroupService, Depends()],
    msg: str = None,
):
    page_params.order_field = "code"
    groups, total = service.read_all_paginated(page_params, filter)
    page = PageResponse(page=page_params.page, size=page_params.size, total=total, content=groups)
    context = page.model_dump()
    context |= filter.model_dump()
    context |= {
        "query_params": f"&size={page_params.size}&order_field={page_params.order_field}"
        + f"&direction={page_params.direction.value}&target={filter.target if filter.target else ''}"
    }
    context |= {"msg": msg, "type": "success"}
    return main.templates.TemplateResponse(request=request, name="core/group_list.html", context=context)


@router.get("/create")
async def group_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/group_create.html", context={})


@router.post("/create")
async def group_create_perform(
    request: Request,
    service: Annotated[GroupService, Depends()],
):
    form = GroupCreateForm(request)
    await form.load()
    if not form.is_valid():
        return main.templates.TemplateResponse(request=request, name="core/group_create.html", context=form.__dict__)
    service.create(GroupCreateCommand.model_validate({"code": form.code, "webname": form.webname}))
    redirect_ulr = request.url_for("group_list").include_query_params(msg="Successful operation")
    return RedirectResponse(redirect_ulr, 303)
