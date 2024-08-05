from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import (
    GroupCreateCommand,
    GroupFilter,
    GroupResponse,
    GroupSimpleResponse,
    PageParams,
    PageResponse,
)
from src.app.modules.core.domain.group_service import GroupService


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
    return PageResponse(page=page_params.page, size=page_params.size, total=total, content=groups)


@router.get("/index", response_model=list[GroupSimpleResponse])
async def read_index(service: Annotated[GroupService, Depends()]):
    groups = service.read_all()
    return groups


@router.get("/{id}", response_model=GroupResponse)
async def read_by_id(id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return group
