from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.persistence.permission_repo import PermissionRepo
from src.app.modules.core.persistence.resource_repo import ResourceRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.modules.core.domain.models import (
    Permission,
    PermissionCreateCommand,
    Resource,
    Role,
    RoleCommand,
    RoleFilter,
)
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.utils.paginator import PageParams
from src.app.configuration.lang import tr


class RoleService:

    def __init__(
        self,
        repo: Annotated[RoleRepo, Depends()],
        permission_repo: Annotated[PermissionRepo, Depends()],
        resource_repo: Annotated[ResourceRepo, Depends()],
        locale: Locale,
    ) -> None:
        self.repo = repo
        self.permission_repo = permission_repo
        self.resource_repo = resource_repo
        self.locale = locale

    def create(self, command: RoleCommand) -> Role:
        try:
            role = Role.model_validate(command)
            return self.repo.create(role)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def read_by_id(self, id: str) -> Role:
        role = self.repo.read_by_id(id)
        if role is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return role

    def read_all(self) -> list[Role]:
        roles = self.repo.read_all()
        return roles

    def read_all_paginated(self, page_params: PageParams, filter: RoleFilter) -> tuple[list[Role], int]:
        total = self.repo.count_all_filtered(filter)
        roles = self.repo.read_paginated(page_params, filter)
        return (roles, total)

    def update(self, id: str, command: RoleCommand):
        try:
            role = Role.model_validate(command)
            role.id = id
            role_updated = self.repo.update(id, role)
            if role_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return role_updated
        except EntityAlreadyExistsError as e:
            e.msg = "Role code already exists"
            raise e

    def delete(self, id: str) -> None:
        try:
            role = self.repo.delete(id)
            if role is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e

    def create_permission(self, role_id: str, command: PermissionCreateCommand):
        try:
            resource = self.__validate_permission_command(command)
            role = self.read_by_id(role_id)
            permission_dict = command.model_dump()
            permission_dict.update({"role": role, "resource": resource})
            permission = Permission(**permission_dict, role_id=role_id)
            permission = Permission.model_validate(permission)
            return self.permission_repo.create(permission)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=f"r:{role_id} res:{command.resource_id}")
            raise e

    def read_role_permission_index(self, role_id: str):
        role = self.read_by_id(role_id)
        permissions = self.permission_repo.read_all_by_role(role)
        return permissions

    def __validate_permission_command(self, command: PermissionCreateCommand) -> Resource:
        if command.resource_id:
            resource = self.resource_repo.read_by_id(command.resource_id)
            if resource is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.resource_id))
        return resource or None
