from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.dependencies import principal
from src.app.modules.core.domain.models import (
    ConfigurationValueCommand,
    ConfigurationValueResponse,
    GroupCreateCommand,
    GroupFilter,
    GroupResponse,
    GroupResponseWithRels,
    GroupSimpleResponse,
    GroupUpdateCommand,
)
from src.app.modules.core.domain.services.group_service import GroupService
from src.app.modules.core.utils.paginator import PageParser, PageResponse, PageParams


router = APIRouter(prefix="/api/core/groups", tags=["Core - Groups"])


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create(command: GroupCreateCommand, service: Annotated[GroupService, Depends()]):
    group = service.create(command)
    return group


@router.get("/", response_model=PageResponse[GroupResponse])
async def read(
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[GroupFilter, Depends()],
    service: Annotated[GroupService, Depends()],
):
    groups, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(groups, GroupResponse)
    return parser.generate_page_response(page=page_params.page, size=page_params.size, total=total)


@router.get("/index", response_model=list[GroupSimpleResponse], dependencies=[Depends(principal)])
async def read_index(service: Annotated[GroupService, Depends()]):
    groups = service.read_all()
    return groups


@router.get("/{id}", response_model=GroupResponse)
async def read_by_id(id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return group


@router.put("/{id}", response_model=GroupResponse)
async def update(id: str, command: GroupUpdateCommand, service: Annotated[GroupService, Depends()]):
    group = service.update(id, command)
    return group


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[GroupService, Depends()]):
    service.delete(id)


@router.patch("/{id}/modules", response_model=GroupResponseWithRels)
async def update_modules(id: str, command: list[str], service: Annotated[GroupService, Depends()]):
    group = service.update_modules(id, command)
    return group


@router.post(
    "/{id}/configuration-values", response_model=ConfigurationValueResponse, status_code=status.HTTP_201_CREATED
)
async def create_configuration_value(
    id: str, command: ConfigurationValueCommand, service: Annotated[GroupService, Depends()]
):
    configuration_value = service.create_configuration_value(id, command)
    return configuration_value


@router.get("/{id}/configuration-values/index", response_model=list[ConfigurationValueResponse])
async def read_configuration_values_index(id: str, service: Annotated[GroupService, Depends()]):
    configuration_values = service.read_configuration_values_index(id)
    return configuration_values
