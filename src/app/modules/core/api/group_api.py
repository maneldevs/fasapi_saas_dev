from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import GroupCreateCommand, GroupResponse
from src.app.modules.core.domain.group_service import GroupService


router = APIRouter(prefix="/api/core/groups", tags=["Core - Groups"])


@router.post("/", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
async def create(command: GroupCreateCommand, service: Annotated[GroupService, Depends()]):
    group = service.create(command)
    return group


@router.get("/{id}", response_model=GroupResponse)
async def readById(id: str, service: Annotated[GroupService, Depends()]):
    group = service.read_by_id(id)
    return group
