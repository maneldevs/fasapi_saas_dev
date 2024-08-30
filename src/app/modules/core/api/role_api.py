from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import (
    PermissionCreateCommand,
    PermissionResponse,
    PermissionSimpleResponse,
    RoleCommand,
    RoleFilter,
    RoleResponse,
)
from src.app.modules.core.domain.services.role_service import RoleService
from src.app.modules.core.utils.paginator import PageParams, PageParser, PageResponse


router = APIRouter(prefix="/api/core/roles", tags=["Core - Roles"])


@router.post("/", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def create(command: RoleCommand, service: Annotated[RoleService, Depends()]):
    role = service.create(command)
    return role


@router.get("/", response_model=PageResponse[RoleResponse])
async def read(
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[RoleFilter, Depends()],
    service: Annotated[RoleService, Depends()],
):
    roles, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(roles, RoleResponse)
    return parser.generate_page_response(page=page_params.page, size=page_params.size, total=total)


@router.get("/index", response_model=list[RoleResponse])
async def read_index(service: Annotated[RoleService, Depends()]):
    roles = service.read_all()
    return roles


@router.get("/{id}", response_model=RoleResponse)
async def read_by_id(id: str, service: Annotated[RoleService, Depends()]):
    role = service.read_by_id(id)
    return role


@router.put("/{id}", response_model=RoleResponse)
async def update(id: str, command: RoleCommand, service: Annotated[RoleService, Depends()]):
    role = service.update(id, command)
    return role


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[RoleService, Depends()]):
    service.delete(id)


@router.post("/{id}/permissions", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
async def create_role_permission(id: str, command: PermissionCreateCommand, service: Annotated[RoleService, Depends()]):
    permission = service.create_permission(id, command)
    return permission


@router.get("/{id}/permissions/index", response_model=list[PermissionSimpleResponse])
async def read_role_permissions_index(id: str, service: Annotated[RoleService, Depends()]):
    permissions = service.read_role_permission_index(id)
    return permissions
