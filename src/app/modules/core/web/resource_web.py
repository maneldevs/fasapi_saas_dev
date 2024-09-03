from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form, ResourceForm
from src.app.modules.core.domain.models import ResourceUpdateCommand
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.domain.services.resource_service import ResourceService


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
async def resource_update_perform(request: Request, id: str, service: Annotated[ResourceService, Depends()]):
    form = ResourceForm(request, ResourceUpdateCommand)
    context = {"id": id}
    command, errors_dict, response = await form.perform_validation("resource_update_perform", context)
    if errors_dict:
        return response
    params = {"id": id, "command": command}
    return await form.perform_action(
        lambda: service.update(**params),
        "module_resource_list",
        {"id": command.module_id},
        "resource_update_perform",
        context,
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
