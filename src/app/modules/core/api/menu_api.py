from typing import Annotated
from fastapi import APIRouter, Depends, status

from src.app.modules.core.domain.models import MenuCommand, MenuResponse, MenuSimpleResponse
from src.app.modules.core.domain.services.menu_service import MenuService


router = APIRouter(prefix="/api/core/menus", tags=["Core - Menus"])


@router.get("/tree", response_model=list[MenuResponse])
async def read_tree(service: Annotated[MenuService, Depends()]):
    menus = service.read_all_root()
    return menus


@router.get("/{id}", response_model=MenuSimpleResponse)
async def read_by_id(id: str, service: Annotated[MenuService, Depends()]):
    menu = service.read_by_id(id)
    return menu


@router.post("/", response_model=MenuSimpleResponse, status_code=status.HTTP_201_CREATED)
async def create(command: MenuCommand, service: Annotated[MenuService, Depends()]):
    menu = service.create(command)
    return menu


@router.put("/{id}", response_model=MenuSimpleResponse)
async def update(id: str, command: MenuCommand, service: Annotated[MenuService, Depends()]):
    menu = service.update(id, command)
    return menu


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: str, service: Annotated[MenuService, Depends()]):
    service.delete(id)
