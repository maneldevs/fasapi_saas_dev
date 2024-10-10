from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.forms import Form
from src.app.modules.core.domain.models import ConfigurationValueCommand, ConfigurationValueUpdateCommand
from src.app.modules.core.domain.services.configuration_value_service import ConfigurationValueService
from src.app.modules.core.domain.services.group_service import GroupService


router = APIRouter(prefix="/core/configuration-value", dependencies=[Depends(principal_god)])


@router.post("/upsert")
async def configuration_value_upsert_perform(
    request: Request,
    service: Annotated[ConfigurationValueService, Depends()],
    group_service: Annotated[GroupService, Depends()],
):
    data = await request.form()
    id = data.get("id")
    configuration_id = data.get("configuration_id")
    value = data.get("value")
    group_id = data.get("group_id")
    update = id is not None and id != "None"
    form = Form(request)
    redirect_params = {"id": group_id}
    url = request.url_for("group_configuration_values", **redirect_params)
    if update:
        command = ConfigurationValueUpdateCommand(value=value)
        params = {"id": id, "command": command}
        response = await form.perform_action_by_url(func=lambda: service.update(**params), url_ok=url, url_nok=url)
    else:
        command = ConfigurationValueCommand(value=value, configuration_id=configuration_id)
        params = {"id": group_id, "command": command}
        response = await form.perform_action_by_url(
            func=lambda: group_service.create_configuration_value(**params), url_ok=url, url_nok=url
        )
    return response
