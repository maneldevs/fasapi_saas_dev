from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.modules.core.domain.models import Role, RoleCommand, RoleFilter
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.utils.paginator import PageParams
from src.app.configuration.lang import tr


class RoleService:

    def __init__(self, repo: Annotated[RoleRepo, Depends()], locale: Locale) -> None:
        self.repo = repo
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
