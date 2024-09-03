from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi import Form as FForm
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.models import GroupCreateCommand, GroupFilter, GroupResponse, GroupUpdateCommand
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.utils.paginator import PageParams, PageParser
from src.app.modules.core.domain.forms import Form, GroupCreateForm, GroupUpdateForm

router = APIRouter(prefix="/core/groups", dependencies=[Depends(principal_god)])


@router.get("/")
async def group_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[GroupFilter, Depends()],
    service: Annotated[GroupService, Depends()],
    msg: str = None,
    type: str = "success",
):
    page_params.order_field = "code"
    groups, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(groups, GroupResponse)
    context = parser.generate_web_context(page_params, total, filter, msg, type)
    return main.templates.TemplateResponse(request=request, name="core/group_list.html", context=context)


@router.get("/create")
async def group_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/group_create.html", context={})


@router.post("/create")
async def group_create_perform(request: Request, service: Annotated[GroupService, Depends()]):
    form = GroupCreateForm(request, GroupCreateCommand)
    command, errors_dict, response = await form.perform_validation("group_create_perform", {})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(lambda: service.create(**params), "group_list", {}, "group_create_perform", {})


@router.get("/update/{id}")
async def group_update(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/group_update.html", context=group.model_dump())


@router.post("/update/{id}")
async def group_update_perform(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    form = GroupUpdateForm(request, GroupUpdateCommand)
    command, errors_dict, response = await form.perform_validation("group_update_perform", {"id": id})
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params), "group_list", {}, "group_update_perform", {"id": id}
    )


@router.post("/delete/{id}")
async def group_delete_perform(request: Request, id: str, service: Annotated[GroupService, Depends()]):
    form = Form(request)
    params = {"id": id}
    return await form.perform_action(lambda: service.delete(**params), "group_list", {}, "group_list", {})


@router.get("/update-modules/{id}")
async def group_update_modules(
    request: Request,
    id: str,
    service: Annotated[GroupService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
):
    group = service.read_by_id(id)
    all_modules = module_service.read_all()
    modules = [{"id": m.id, "webname": m.webname, "active": m in group.modules} for m in all_modules]
    return main.templates.TemplateResponse(
        request=request,
        name="core/group_modules.html",
        context={"id": group.id, "name": group.webname, "modules": modules},
    )


@router.post("/update-modules/{id}")
async def group_update_modules_perform(
    request: Request,
    id: str,
    service: Annotated[GroupService, Depends()],
    module_selected_ids: Annotated[list[str], FForm()] = [],
):
    form = Form(request)
    params = {"id": id, "command": module_selected_ids}
    return await form.perform_action(
        lambda: service.update_modules(**params),
        "group_list",
        {},
        "group_update_modules_perform",
        {"id": id, "module_selected_ids": module_selected_ids},
    )
