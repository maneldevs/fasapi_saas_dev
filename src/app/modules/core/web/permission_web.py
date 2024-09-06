from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form
from src.app.modules.core.domain.models import PermissionCreateCommand, PermissionFilter, PermissionUpdateCommand
from src.app.modules.core.domain.services.permission_service import PermissionService
from src.app.modules.core.domain.services.role_service import RoleService


router = APIRouter(prefix="/core/permission", dependencies=[Depends(principal_god)])


@router.post("/upsert")
async def permission_upsert_perform(
    request: Request, service: Annotated[PermissionService, Depends()], role_service: Annotated[RoleService, Depends()]
):
    data = await request.form()
    id = data.get("id")
    scope = data.get("scope")
    scope_owner = data.get("scope_owner")
    role_id = data.get("role_id")
    resource_id = data.get("resource_id")
    module_id = data.get("module_id")
    update = id is not None and id != "None"
    form = Form(request)
    redirect_params = {"id": role_id}
    url = request.url_for("role_permissions", **redirect_params).include_query_params(module_id=module_id)
    if update:
        command = PermissionUpdateCommand(scope=scope, scope_owner=scope_owner)
        params = {"id": id, "command": command}
        response = await form.perform_action_by_url(func=lambda: service.update(**params), url_ok=url, url_nok=url)
    else:
        command = PermissionCreateCommand(resource_id=resource_id, scope=scope, scope_owner=scope_owner)
        params = {"role_id": role_id, "command": command}
        response = await form.perform_action_by_url(
            func=lambda: role_service.create_permission(**params), url_ok=url, url_nok=url
        )
    return response
