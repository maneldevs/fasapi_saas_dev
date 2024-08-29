from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import ResourceResponse, ResourceUpdateCommand
from src.app.modules.core.domain.services.resource_service import ResourceService


router = APIRouter(prefix="/api/core/resources", tags=["Core - Resources"])


@router.get("/{id}", response_model=ResourceResponse)
async def read_by_id(id: str, service: Annotated[ResourceService, Depends()]):
    resource = service.read_by_id(id)
    return resource


@router.put("/{id}", response_model=ResourceResponse)
async def update(id: str, command: ResourceUpdateCommand, service: Annotated[ResourceService, Depends()]):
    resource = service.update(id, command)
    return resource


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[ResourceService, Depends()]):
    service.delete(id)
