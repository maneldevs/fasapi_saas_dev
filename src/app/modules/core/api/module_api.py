from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import ModuleCommand, ModuleFilter, ModuleResponse
from src.app.modules.core.domain.services.module_service import ModuleService
from src.app.modules.core.utils.paginator import PageParams, PageParser, PageResponse


router = APIRouter(prefix="/api/core/modules", tags=["Core - Modules"])


@router.post("/", response_model=ModuleResponse, status_code=status.HTTP_201_CREATED)
async def create(command: ModuleCommand, service: Annotated[ModuleService, Depends()]):
    module = service.create(command)
    return module


@router.get("/", response_model=PageResponse[ModuleResponse])
async def read(
    page_params: Annotated[PageParams, Depends()],
    filter: Annotated[ModuleFilter, Depends()],
    service: Annotated[ModuleService, Depends()],
):
    modules, total = service.read_all_paginated(page_params, filter)
    parser = PageParser(modules, ModuleResponse)
    return parser.generate_page_response(page=page_params.page, size=page_params.size, total=total)


@router.get("/index", response_model=list[ModuleResponse])
async def read_index(service: Annotated[ModuleService, Depends()]):
    modules = service.read_all()
    return modules


@router.get("/{id}", response_model=ModuleResponse)
async def read_by_id(id: str, service: Annotated[ModuleService, Depends()]):
    module = service.read_by_id(id)
    return module


@router.put("/{id}", response_model=ModuleResponse)
async def update(id: str, command: ModuleCommand, service: Annotated[ModuleService, Depends()]):
    module = service.update(id, command)
    return module


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[ModuleService, Depends()]):
    service.delete(id)