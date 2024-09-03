from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form, ResourceForm
from src.app.modules.core.domain.models import ModuleResponse, ResourceCreateCommand, ResourceUpdateCommand
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.domain.services.resource_service import ResourceService
from src.app.modules.core.utils.paginator import PageParser



router = APIRouter(prefix="/core/resources", dependencies=[Depends(principal_god)])


@router.get("/{id}/update")
async def module_resource_update(
    request: Request,
    id: str,
    service: Annotated[ResourceService, Depends()],
    module_service: Annotated[ModuleService, Depends()],
):
    resource = service.read_by_id(id)
    modules = __fetch_modules(module_service)
    context = {"modules": modules}
    context |= resource.model_dump()
    return main.templates.TemplateResponse(request=request, name="core/module_resource_update.html", context=context)


@router.post("/{id}/update")
async def resource_update_perform(
    request: Request, id: str, service: Annotated[ResourceService, Depends()]
):
    # resource_to_update = service.read_by_id(id)
    # module = resource_to_update.module
    # module_copy = module.__class__(**module.model_dump())
    # resources = module.resources
    # resources.sort(key=lambda r: r.code)
    # resources_copy = [r.__class__(**r.model_dump()) for r in resources]
    # context = {"module": module_copy, "resources": resources_copy}
    # form = ResourceForm(request, ResourceUpdateCommand, "core/module_resource_list.html")
    # command, errors_dict, response, context = await form.validate(context)
    # if errors_dict:
    #     return response
    # params = {"id": id, "command": command}
    # return await form.perform_operation(service.update, params, "module_resource_list", context, id=module_id)
    form = ResourceForm(request, ResourceUpdateCommand)
    context = {"id": id}
    command, errors_dict, response = await form.perform_validation("resource_update_perform", context)
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params), "module_resource_list", {"id": command.module_id}, "resource_update_perform", context
    )


@router.post("/delete/{id}")
async def resource_delete_perform(request: Request, id: str, service: Annotated[ResourceService, Depends()]):
    resource = service.read_by_id(id)
    form = Form(request)
    params = {"id": id}
    context = {"id": resource.module.id}
    return await form.perform_action(
        lambda: service.delete(**params), "module_resource_list", context, "module_resource_list", context
    )


def __fetch_modules(service_module: ModuleService):
    modules_in_db = service_module.read_all()
    modules_in_db.sort(key=lambda r: r.code)
    return modules_in_db
