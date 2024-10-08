from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.models import ModuleCommand, ModuleFilter, ModuleResponse, ResourceCreateCommand
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.utils.paginator import PageParams, PageParser
from src.app.modules.core.domain.forms import Form, ModuleForm, ResourceForm

router = APIRouter(prefix="/core/modules", dependencies=[Depends(principal_god)])


@router.get("/")
async def module_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[ModuleFilter, Depends()],
    service: Annotated[ModuleService, Depends()],
):
    page_params.order_field = "code"
    modules, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(modules, ModuleResponse)
    context = parser.generate_web_context(page_params, total, filter)
    return main.templates.TemplateResponse(request=request, name="core/module_list.html", context=context)


@router.get("/create")
async def module_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/module_create.html", context={})


@router.post("/create")
async def module_create_perform(request: Request, service: Annotated[ModuleService, Depends()]):
    form = ModuleForm(request, ModuleCommand)
    command, errors_dict, response = await form.perform_validation("module_create_perform", {})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(lambda: service.create(**params), "module_list", {}, "module_create_perform", {})


@router.get("/update/{id}")
async def module_update(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    module = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/module_update.html", context=module.model_dump())


@router.post("/update/{id}")
async def module_update_perform(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    form = ModuleForm(request, ModuleCommand)
    command, errors_dict, response = await form.perform_validation("module_update_perform", {"id": id})
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params), "module_list", {}, "module_update_perform", {"id": id}
    )


@router.post("/delete/{id}")
async def module_delete_perform(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    form = Form(request)
    params = {"id": id}
    return await form.perform_action(lambda: service.delete(**params), "module_list", {}, "module_list", {})


@router.get("/{id}/resources")
async def module_resource_list(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    module = service.read_by_id(id)
    resources = module.resources
    resources.sort(key=lambda r: r.code)
    context = {"module": module, "resources": resources}
    return main.templates.TemplateResponse(request=request, name="core/module_resource_list.html", context=context)


@router.get("/{id}/resources/create")
async def module_resource_create(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    module = service.read_by_id(id)
    context = {"module": module}
    return main.templates.TemplateResponse(request=request, name="core/module_resource_create.html", context=context)


@router.post("/{id}/resources/create")
async def resource_create_perform(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    form = ResourceForm(request, ResourceCreateCommand)
    context = {"id": id}
    command, errors_dict, response = await form.perform_validation("resource_create_perform", context)
    if errors_dict:
        return response
    params = {"module_id": id, "command": command}
    return await form.perform_action(
        lambda: service.create_resource(**params), "module_resource_list", context, "resource_create_perform", context
    )
