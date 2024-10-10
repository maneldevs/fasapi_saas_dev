from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import ConfigurationForm, Form
from src.app.modules.core.domain.models import ConfigurationCommand
from src.app.modules.core.domain.services.configuration_service import ConfigurationService
from src.app.modules.core.domain.services.module_service import ModuleService


router = APIRouter(prefix="/core/configurations", dependencies=[Depends(principal_god)])


@router.get("/")
async def configuration_list(request: Request, service: Annotated[ConfigurationService, Depends()]):
    configurations = service.read_all()
    context = {"configurations": configurations}
    return main.templates.TemplateResponse(request=request, name="core/configuration_list.html", context=context)


@router.get("/create")
async def configuration_create(request: Request, module_service: Annotated[ModuleService, Depends()]):
    modules = module_service.read_all()
    context = {"modules": modules}
    return main.templates.TemplateResponse(request=request, name="core/configuration_create.html", context=context)


@router.post("/create")
async def configuration_create_perform(request: Request, service: Annotated[ConfigurationService, Depends()]):
    form = ConfigurationForm(request, ConfigurationCommand)
    command, errors_dict, response = await form.perform_validation("configuration_create_perform", {})
    if errors_dict:
        return response
    params = {"command": command}
    return await form.perform_action(
        lambda: service.create(**params), "configuration_list", {}, "configuration_create_perform", {}
    )


@router.get("/update/{id}")
async def configuration_update(
    request: Request,
    id: str,
    service: Annotated[ConfigurationService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
):
    modules = module_service.read_all()
    configuration = service.read_by_id(id)
    context = {"configuration": configuration, "modules": modules}
    return main.templates.TemplateResponse(
        request=request, name="core/configuration_update.html", context=context
    )


@router.post("/update/{id}")
async def configuration_update_perform(request: Request, id: str, service: Annotated[ConfigurationService, Depends()]):
    form = ConfigurationForm(request, ConfigurationCommand)
    command, errors_dict, response = await form.perform_validation("configuration_update_perform", {"id": id})
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params), "configuration_list", {}, "configuration_update_perform", {"id": id}
    )


@router.post("/delete/{id}")
async def configuration_delete_perform(request: Request, id: str, service: Annotated[ConfigurationService, Depends()]):
    form = Form(request)
    params = {"id": id}
    return await form.perform_action(
        lambda: service.delete(**params), "configuration_list", {}, "configuration_list", {}
    )
