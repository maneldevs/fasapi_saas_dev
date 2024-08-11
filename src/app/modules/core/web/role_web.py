from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.models import RoleCommand, RoleFilter
from src.app.modules.core.domain.services.role_service import RoleService
from src.app.modules.core.utils.paginator import PageParams, PageResponse
from src.app.modules.core.domain.forms import Form, RoleForm

router = APIRouter(prefix="/core/roles")


@router.get("/")
async def role_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[RoleFilter, Depends()],
    service: Annotated[RoleService, Depends()],
    msg: str = None,
):
    page_params.order_field = "code"
    roles, total = service.read_all_paginated(page_params, filter)
    page = PageResponse(page=page_params.page, size=page_params.size, total=total, content=roles)
    context = page.model_dump()
    context |= filter.model_dump()
    context |= {
        "query_params": f"&size={page_params.size}&order_field={page_params.order_field}"
        + f"&direction={page_params.direction.value}&target={filter.target if filter.target else ''}"
    }
    context |= {"msg": msg, "type": "success"}
    return main.templates.TemplateResponse(request=request, name="core/role_list.html", context=context)


@router.get("/create")
async def role_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/role_create.html", context={})


@router.post("/create")
async def role_create_perform(request: Request, service: Annotated[RoleService, Depends()]):
    form = RoleForm(request)
    command = RoleCommand.model_validate(await form.load())
    params = {"command": command}
    return await form.perform_operation(service.create, params, "core/role_create.html", "role_list")


@router.get("/update/{id}")
async def role_update(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    role = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/role_update.html", context=role.model_dump())


@router.post("/update/{id}")
async def role_update_perform(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    form = RoleForm(request)
    command = RoleCommand.model_validate(await form.load())
    params = {"id": id, "command": command}
    return await form.perform_operation(service.update, params, "core/role_update.html", "role_list")


@router.post("/delete/{id}")
async def role_delete_perform(request: Request, id: str, service: Annotated[RoleService, Depends()]):
    form = Form(request)
    await form.load()
    params = {"id": id}
    return await form.perform_operation(service.delete, params, "core/role_list.html", "role_list")