from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi import Form as FForm
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.models import Permission, PermissionFilter, RoleCommand, RoleFilter, RoleResponse
from src.app.modules.core.domain.services.menu_service import MenuService
from src.app.modules.core.domain.services.module_service import ModuleService
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


@router.get("/{id}/permissions")
async def role_permissions(
    request: Request,
    id: str,
    service: Annotated[RoleService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
    filter: Annotated[PermissionFilter, Depends()] = None,
):
    module_id = filter.module_id if filter and filter.module_id else None
    modules = module_service.read_all()
    role = service.read_by_id(id)
    resources = []
    permissions = []
    data = []
    if filter and filter.module_id:
        resources = module_service.read_module_resource_index(filter.module_id)
        resources.sort(key=lambda r: r.code)
        permissions = service.read_role_permission_index(id, filter)
        for resource in resources:
            permission_as_list = [p for p in permissions if p.resource_id == resource.id]
            if permission_as_list and len(permission_as_list) > 0:
                permission = permission_as_list[0]
            else:
                permission = Permission(
                    id=None,
                    scope=None,
                    scope_owner=None,
                    role_id=id,
                    role=role,
                    resource_id=resource.id,
                    resource=resource,
                )
            data.append({"resource": resource, "permission": permission})
    context = {"module_id": module_id, "modules": modules, "role": role, "data": data}
    return main.templates.TemplateResponse(request=request, name="core/role_permissions.html", context=context)


@router.get("/{id}/menus")
async def role_menus(
    request: Request,
    id: str,
    service: Annotated[RoleService, Depends()],
    menu_service: Annotated[MenuService, Depends()],
):
    role = service.read_by_id(id)
    menu_roots = menu_service.read_all_root()
    role_menus = []
    role_menus += role.menus
    role_menu_ids = [menu.id for menu in role_menus]
    context = {"role": role, "menu_roots": menu_roots, "role_menu_ids": role_menu_ids}
    return main.templates.TemplateResponse(request=request, name="core/role_menus.html", context=context)


@router.post("/{id}/menus")
async def role_menus_perform(
    request: Request,
    id: str,
    service: Annotated[RoleService, Depends()],
    menu_root_selected_ids: Annotated[list[str], FForm()] = [],
    menu_child_selected_ids: Annotated[list[str], FForm()] = [],
):
    form = Form(request)
    menu_ids = []
    menu_ids += menu_root_selected_ids
    menu_ids += menu_child_selected_ids
    params = {"id": id, "command": menu_ids}
    return await form.perform_action(
        lambda: service.update_menus(**params),
        "role_list",
        {},
        "role_menus",
        {"id": id},
    )
