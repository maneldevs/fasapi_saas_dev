from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form, ResourceForm
from src.app.modules.core.domain.models import ResourceCreateCommand, ResourceUpdateCommand
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.domain.services.resource_service import ResourceService


router = APIRouter(prefix="/core/resources", dependencies=[Depends(principal_god)])


@router.post("/create/module/{module_id}")
async def resource_create_perform(
    request: Request, module_id: str, module_service: Annotated[ModuleService, Depends()]
):
    module = module_service.read_by_id(module_id)
    module_copy = module.__class__(**module.model_dump())
    resources = module.resources
    resources.sort(key=lambda r: r.code)
    resources_copy = [r.__class__(**r.model_dump()) for r in resources]
    context = {"module": module_copy, "resources": resources_copy}
    form = ResourceForm(request, ResourceCreateCommand, "core/module_resource_list.html")
    command, errors_dict, response, context = await form.validate(context)
    if errors_dict:
        return response
    params = {"module_id": module_id, "command": command}
    return await form.perform_operation(
        module_service.create_resource, params, "module_resource_list", context, id=module_id
    )


@router.post("/update/{id}/module/{module_id}")
async def resource_update_perform(
    request: Request, id: str, module_id: str, service: Annotated[ResourceService, Depends()]
):
    resource_to_update = service.read_by_id(id)
    module = resource_to_update.module
    module_copy = module.__class__(**module.model_dump())
    resources = module.resources
    resources.sort(key=lambda r: r.code)
    resources_copy = [r.__class__(**r.model_dump()) for r in resources]
    context = {"module": module_copy, "resources": resources_copy}
    form = ResourceForm(request, ResourceUpdateCommand, "core/module_resource_list.html")
    # form.flash_message("todo ok", "success")
    # form.flash_validation_errors({"error1": "error1v", "error2": "error2v"})
    # message = Form.unflash_message(request)
    # errs = Form.unflash_validation_errors(request)
    command, errors_dict, response, context = await form.validate(context)
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_operation(
        service.update, params, "module_resource_list", context, id=module_id
    )


@router.post("/delete/{id}")
async def resource_delete_perform(request: Request, id: str, service: Annotated[ResourceService, Depends()]):
    resource = service.read_by_id(id)
    form = Form(request)
    params = {"id": id}
    return await form.perform_delete(service.delete, params, "module_resource_list", id=resource.module.id)
