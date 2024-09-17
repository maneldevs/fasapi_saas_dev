from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form, MenuForm
from src.app.modules.core.domain.models import MenuCommand
from src.app.modules.core.domain.services.menu_service import MenuService
from src.app.modules.core.domain.services.module_service import ModuleService


router = APIRouter(prefix="/core/menus", dependencies=[Depends(principal_god)])


@router.get("/")
async def menu_tree(request: Request, service: Annotated[MenuService, Depends()]):
    menu_roots = service.read_all_root()
    context = {"menu_roots": menu_roots}
    return main.templates.TemplateResponse(request=request, name="core/menu_tree.html", context=context)


@router.get("/create")
async def menu_create(
    request: Request,
    service: Annotated[MenuService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
    parent_id: str | None = None,
):
    modules = module_service.read_all()
    parent = None
    if parent_id:
        parent = service.read_by_id(parent_id)
    context = {"parent": parent, "modules": modules}
    return main.templates.TemplateResponse(request=request, name="core/menu_create.html", context=context)


@router.post("/create")
async def menu_create_perform(request: Request, service: Annotated[MenuService, Depends()]):
    form = MenuForm(request, MenuCommand)
    command, errors_dict, response = await form.perform_validation("menu_create", {})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(lambda: service.create(**params), "menu_tree", {}, "menu_create", {})


@router.get("/submenu_create/{parent_id}")
async def submenu_create(
    request: Request,
    service: Annotated[MenuService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
    parent_id: str,
):
    modules = module_service.read_all()
    menu_roots = service.read_all_root()
    parent = None
    if parent_id:
        parent = service.read_by_id(parent_id)
    context = {"parent": parent, "modules": modules, "menu_roots": menu_roots}
    return main.templates.TemplateResponse(request=request, name="core/menu_child_create.html", context=context)


@router.post("/submenu_create")
async def submenu_create_perform(request: Request, service: Annotated[MenuService, Depends()]):
    form = MenuForm(request, MenuCommand)
    parent_id = (await request.form()).get("parent_id")
    command, errors_dict, response = await form.perform_validation("submenu_create", {"parent_id": parent_id})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(
        lambda: service.create(**params), "menu_tree", {}, "submenu_create", {"parent_id": parent_id}
    )


@router.get("/update/{id}")
async def menu_update(
    request: Request,
    id: str,
    service: Annotated[MenuService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
):
    modules = module_service.read_all()
    menu = service.read_by_id(id)
    menu_roots = service.read_all_root()
    context = {"menu": menu, "modules": modules, "menu_roots": menu_roots}
    return main.templates.TemplateResponse(request=request, name="core/menu_update.html", context=context)


@router.post("/update/{id}")
async def menu_update_perform(request: Request, id: str, service: Annotated[MenuService, Depends()]):
    form = MenuForm(request, MenuCommand)
    command, errors_dict, response = await form.perform_validation("menu_update", {"id": id})
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(lambda: service.update(**params), "menu_tree", {}, "menu_update", {"id": id})


@router.post("/delete/{id}")
async def menu_delete_perform(request: Request, id: str, service: Annotated[MenuService, Depends()]):
    form = Form(request)
    params = {"id": id}
    return await form.perform_action(lambda: service.delete(**params), "menu_tree", {}, "menu_tree", {})
