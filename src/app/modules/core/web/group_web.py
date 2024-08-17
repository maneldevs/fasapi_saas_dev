from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import GroupCreateCommand, GroupFilter, GroupResponse, GroupUpdateCommand
from src.app.modules.core.utils.paginator import PageParams, PageParser
from src.app.modules.core.domain.forms import Form, GroupCreateForm, GroupUpdateForm

router = APIRouter(prefix="/core/groups")


@router.get("/", dependencies=[Depends(principal_god)])
async def group_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[GroupFilter, Depends()],
    service: Annotated[GroupService, Depends()],
    msg: str = None,
):
    page_params.order_field = "code"
    groups, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(groups, GroupResponse)
    context = parser.generate_web_context(page_params, total, filter, msg)
    return main.templates.TemplateResponse(request=request, name="core/group_list.html", context=context)


@router.get("/create")
async def group_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/group_create.html", context={})


@router.post("/create")
async def group_create_perform(request: Request, service: Annotated[GroupService, Depends()]):
    form = GroupCreateForm(request)
    command = GroupCreateCommand.model_validate(await form.load())
    params = {"command": command}
    return await form.perform_operation(service.create, params, "core/group_create.html", "group_list")


@router.get("/update/{id}")
async def group_update(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/group_update.html", context=group.model_dump())


@router.post("/update/{id}")
async def group_update_perform(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    form = GroupUpdateForm(request)
    command = GroupUpdateCommand.model_validate(await form.load())
    params = {"id": id, "command": command}
    context = {"id": id}
    return await form.perform_operation(service.update, params, "core/group_update.html", "group_list", context)


@router.post("/delete/{id}")
async def group_delete_perform(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    form = Form(request)
    await form.load()
    params = {"id": id}
    return await form.perform_operation(service.delete, params, "core/group_list.html", "group_list")
