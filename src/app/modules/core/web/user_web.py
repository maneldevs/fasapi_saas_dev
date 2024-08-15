from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.forms import Form, UserCreateForm
from src.app.modules.core.domain.models import (
    GroupSimpleResponse,
    RoleResponse,
    UserCreateCommand,
    UserResponse,
    UserWebFilter,
)
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.domain.services.role_service import RoleService
from src.app.modules.core.domain.services.user_service import UserService
from src.app.modules.core.utils.paginator import PageParams, PageParser


router = APIRouter(prefix="/core/users")


@router.get("/")
async def user_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[UserWebFilter, Depends()],
    service: Annotated[UserService, Depends()],
    service_group: Annotated[GroupService, Depends()],
    msg: str = None,
):
    page_params.order_field = "username"
    users, total = service.read_all_paginated(page_params, filter.parseToUserFilter())
    parser = PageParser(users, UserResponse)
    context = parser.generate_web_context(page_params, total, filter, msg)
    groups = __fetch_groups(service_group)
    context |= {"groups": groups}
    return main.templates.TemplateResponse(request=request, name="core/user_list.html", context=context)


@router.get("/create")
async def user_create(
    request: Request,
    service_group: Annotated[GroupService, Depends()],
    service_role: Annotated[RoleService, Depends()],
):
    groups = __fetch_groups(service_group)
    roles = __fetch_roles(service_role)
    context = {"groups": groups, "roles": roles}
    return main.templates.TemplateResponse(request=request, name="core/user_create.html", context=context)


@router.post("/create")
async def user_create_perform(
    request: Request,
    service: Annotated[UserService, Depends()],
    service_group: Annotated[GroupService, Depends()],
    service_role: Annotated[RoleService, Depends()],
):
    form = UserCreateForm(request)
    command = UserCreateCommand.model_validate(await form.load())
    params = {"command": command}
    groups = __fetch_groups(service_group)
    roles = __fetch_roles(service_role)
    context = {"groups": groups, "roles": roles}
    return await form.perform_operation(service.create, params, "core/user_create.html", "user_list", context)


@router.get("/update/{id}")
async def user_update(
    request: Request,
    id: str,
    service: Annotated[UserService, Depends()],
    service_group: Annotated[GroupService, Depends()],
    service_role: Annotated[RoleService, Depends()],
):
    user = service.read_by_id(id)
    groups = __fetch_groups(service_group)
    roles = __fetch_roles(service_role)
    context = {"groups": groups, "roles": roles}
    context |= user.model_dump()
    return main.templates.TemplateResponse(request=request, name="core/user_update.html", context=context)


@router.post("/delete/{id}")
async def user_delete_perform(request: Request, id: str, service: Annotated[UserService, Depends()]):
    form = Form(request)
    await form.load()
    params = {"id": id}
    return await form.perform_operation(service.delete, params, "core/user_list.html", "user_list")


def __fetch_groups(service_group: GroupService):
    groups_in_db = service_group.read_all()
    parser = PageParser(groups_in_db, GroupSimpleResponse)
    groups = parser.parse_list()
    return groups


def __fetch_roles(service_role: RoleService):
    roles_in_db = service_role.read_all()
    parser = PageParser(roles_in_db, RoleResponse)
    roles = parser.parse_list()
    return roles
