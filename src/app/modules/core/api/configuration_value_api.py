from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import ConfigurationValueResponse, ConfigurationValueUpdateCommand
from src.app.modules.core.domain.services.configuration_value_service import ConfigurationValueService


router = APIRouter(prefix="/api/core/configuration-values", tags=["Core - Configuration Value"])


@router.get("/{id}", response_model=ConfigurationValueResponse)
async def read_by_id(id: str, service: Annotated[ConfigurationValueService, Depends()]):
    configuration_value = service.read_by_id(id)
    return configuration_value


@router.put("/{id}", response_model=ConfigurationValueResponse)
async def update(
    id: str, command: ConfigurationValueUpdateCommand, service: Annotated[ConfigurationValueService, Depends()]
):
    configuration_value = service.update(id, command)
    return configuration_value


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[ConfigurationValueService, Depends()]):
    service.delete(id)
