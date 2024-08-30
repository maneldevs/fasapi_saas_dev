from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import PermissionResponse, PermissionUpdateCommand
from src.app.modules.core.domain.services.permission_service import PermissionService


router = APIRouter(prefix="/api/core/permissions", tags=["Core - Permissions"])


@router.get("/{id}", response_model=PermissionResponse)
async def read_by_id(id: str, service: Annotated[PermissionService, Depends()]):
    permission = service.read_by_id(id)
    return permission


@router.put("/{id}", response_model=PermissionResponse)
async def update(id: str, command: PermissionUpdateCommand, service: Annotated[PermissionService, Depends()]):
    permission = service.update(id, command)
    return permission


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[PermissionService, Depends()]):
    service.delete(id)
