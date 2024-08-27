from typing import Annotated
from fastapi import APIRouter, Depends, Request
from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.models import ModuleCommand, ModuleFilter, ModuleResponse
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.utils.paginator import PageParams, PageParser
from src.app.modules.core.domain.forms import Form, ModuleForm

router = APIRouter(prefix="/core/modules", dependencies=[Depends(principal_god)])


@router.get("/")
async def module_list(
    request: Request,
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[ModuleFilter, Depends()],
    service: Annotated[ModuleService, Depends()],
    msg: str = None,
):
    page_params.order_field = "code"
    modules, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(modules, ModuleResponse)
    context = parser.generate_web_context(page_params, total, filter, msg)
    return main.templates.TemplateResponse(request=request, name="core/module_list.html", context=context)


@router.get("/create")
async def module_create(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/module_create.html", context={})


@router.post("/create")
async def module_create_perform(request: Request, service: Annotated[ModuleService, Depends()]):
    form = ModuleForm(request, ModuleCommand, "core/module_create.html")
    command, errors_dict, response, context = await form.validate()
    if (errors_dict):
        return response
    params = {"command": command}
    return await form.perform_operation(service.create, params, "module_list", context)


@router.get("/update/{id}")
async def module_update(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    module = service.read_by_id(id)
    return main.templates.TemplateResponse(request=request, name="core/module_update.html", context=module.model_dump())


@router.post("/update/{id}")
async def module_update_perform(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    form = ModuleForm(request, ModuleCommand, "core/module_update.html")
    command, errors_dict, response, context = await form.validate()
    if (errors_dict):
        return response
    params = {"id": id, "command": command}
    context |= {"id": id}
    return await form.perform_operation(service.update, params, "module_list", context)


@router.post("/delete/{id}")
async def module_delete_perform(request: Request, id: str, service: Annotated[ModuleService, Depends()]):
    form = Form(request, None, "core/module_list.html")
    params = context = {"id": id}
    return await form.perform_operation(service.delete, params, "module_list", context)
