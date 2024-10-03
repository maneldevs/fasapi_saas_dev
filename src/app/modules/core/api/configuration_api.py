from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import ConfigurationCommand, ConfigurationResponse
from src.app.modules.core.domain.services.configuration_service import ConfigurationService


router = APIRouter(prefix="/api/core/configurations", tags=["Core - Configuration"])


@router.post("/", response_model=ConfigurationResponse, status_code=status.HTTP_201_CREATED)
async def create(command: ConfigurationCommand, service: Annotated[ConfigurationService, Depends()]):
    configuration = service.create(command)
    return configuration


@router.get("/index", response_model=list[ConfigurationResponse])
async def read_index(service: Annotated[ConfigurationService, Depends()]):
    configurations = service.read_all()
    return configurations


@router.get("/{id}", response_model=ConfigurationResponse)
async def read_by_id(id: str, service: Annotated[ConfigurationService, Depends()]):
    configuration = service.read_by_id(id)
    return configuration


@router.put("/{id}", response_model=ConfigurationResponse)
async def update(id: str, command: ConfigurationCommand, service: Annotated[ConfigurationService, Depends()]):
    configuration = service.update(id, command)
    return configuration


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[ConfigurationService, Depends()]):
    service.delete(id)
