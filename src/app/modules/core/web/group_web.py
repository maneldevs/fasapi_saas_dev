from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from src.app import main
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import GroupCreateCommand, GroupFilter, GroupUpdateCommand
from src.app.modules.core.utils.paginator import PageParams, PageResponse
from src.app.modules.core.domain.forms import Form, GroupCreateForm, GroupUpdateForm

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
async def group_create_perform(request: Request, service: Annotated[GroupService, Depends()]):
    form = GroupCreateForm(request)
    command = GroupCreateCommand.model_validate(await form.load())
    params = {"command": command}
    return await __group_save_perform(request, form, service.create, params, "core/group_create.html", "group_list")


@router.get("/update/{id}")
async def group_update(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/group_update.html", context=group.model_dump())


@router.post("/update/{id}")
async def group_update_perform(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    form = GroupUpdateForm(request)
    command = GroupUpdateCommand.model_validate(await form.load())
    params = {"id": id, "command": command}
    return await __group_save_perform(request, form, service.update, params, "core/group_update.html", "group_list")


async def __group_save_perform(request: Request, form: Form, func, params, self_template_path, redirect_method_name):
    form_data = await form.load()
    if form.is_valid():
        try:
            func(**params)
            redirect_ulr = request.url_for(redirect_method_name).include_query_params(msg="Successful operation")
            return RedirectResponse(redirect_ulr, 303)
        except Exception as e:
            form_data |= {"msg": e.msg, "type": "danger"}
    return main.templates.TemplateResponse(request=request, name=self_template_path, context=form_data)
