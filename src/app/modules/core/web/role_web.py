from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.models import RoleCommand, RoleFilter, RoleResponse
from src.app.modules.core.domain.services.role_service import RoleService
from src.app.modules.core.utils.paginator import PageParams, PageParser
from src.app.modules.core.domain.forms import Form, RoleForm

router = APIRouter(prefix="/core/roles", dependencies=[Depends(principal_god)])


@router.get("/")
async def role_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[RoleFilter, Depends()],
    service: Annotated[RoleService, Depends()],
):
    page_params.order_field = "code"
    roles, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(roles, RoleResponse)
    context = parser.generate_web_context(page_params, total, filter)
    return main.templates.TemplateResponse(request=request, name="core/role_list.html", context=context)


@router.get("/create")
async def role_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/role_create.html", context={})


@router.post("/create")
async def role_create_perform(request: Request, service: Annotated[RoleService, Depends()]):
    form = RoleForm(request, RoleCommand)
    command, errors_dict, response = await form.perform_validation("role_create_perform", {})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(lambda: service.create(**params), "role_list", {}, "role_create_perform", {})


@router.get("/update/{id}")
async def role_update(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    role = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/role_update.html", context=role.model_dump())


@router.post("/update/{id}")
async def role_update_perform(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    form = RoleForm(request, RoleCommand)
    command, errors_dict, response = await form.perform_validation("role_update_perform", {"id": id})
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params), "role_list", {}, "role_update_perform", {"id": id}
    )


@router.post("/delete/{id}")
async def role_delete_perform(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    form = Form(request)
    params = {"id": id}
    return await form.perform_action(lambda: service.delete(**params), "role_list", {}, "role_list", {})
