from typing import Annotated

from fastapi import Depends

from src.app.configuration.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.app.modules.core.domain.models import Role, RoleCommand, RoleFilter
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.utils.paginator import PageParams


class RoleService:

    def __init__(self, repo: Annotated[RoleRepo, Depends()]) -> None:
        self.repo = repo

    def create(self, command: RoleCommand) -> Role:
        try:
            role = Role.model_validate(command)
            return self.repo.create(role)
        except EntityAlreadyExistsError as e:
            e.msg = "Role code already exists"
            raise e

    def read_by_id(self, id: str) -> Role:
        role = self.repo.read_by_id(id)
        if role is None:
            raise EntityNotFoundError(msg="Role not found")
        return role

    def read_all(self) -> list[Role]:
        roles = self.repo.read_all()
        return roles

    def read_all_paginated(self, page_params: PageParams, filter: RoleFilter) -> tuple[list[Role], int]:
        total = self.repo.count_all()
        roles = self.repo.read_paginated(page_params, filter)
        return (roles, total)

    def update(self, id: str, command: RoleCommand):
        try:
            role = Role.model_validate(command)
            role.id = id
            role_updated = self.repo.update(id, role)
            if (role_updated is None):
                raise EntityNotFoundError(msg="Role not found")
            return role_updated
        except EntityAlreadyExistsError as e:
            e.msg = "Role code already exists"
            raise e

    def delete(self, id: str) -> None:
        role = self.repo.delete(id)
        if (role is None):
            raise EntityNotFoundError(msg="Role not found")
