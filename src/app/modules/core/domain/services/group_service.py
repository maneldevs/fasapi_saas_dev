from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.modules.core.domain.models import (
    ConfigurationValueCommand,
    Group,
    GroupCreateCommand,
    GroupFilter,
    GroupUpdateCommand,
)
from src.app.modules.core.persistence.group_repo import GroupRepo
from src.app.modules.core.utils.paginator import PageParams
from src.app.configuration.lang import tr


class GroupService:

    def __init__(
        self, repo: Annotated[GroupRepo, Depends()], module_repo: Annotated[ModuleRepo, Depends()], locale: Locale
    ) -> None:
        self.repo = repo
        self.module_repo = module_repo
        self.locale = locale

    def create(self, command: GroupCreateCommand) -> Group:
        try:
            group = Group.model_validate(command)
            return self.repo.create(group)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def read_by_id(self, id: str) -> Group:
        group = self.repo.read_by_id(id)
        if group is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return group

    def read_all(self) -> list[Group]:
        groups = self.repo.read_all()
        return groups

    def read_all_paginated(self, page_params: PageParams, filter: GroupFilter) -> tuple[list[Group], int]:
        total = self.repo.count_all_filetered(filter)
        groups = self.repo.read_paginated(page_params, filter)
        return (groups, total)

    def update(self, id: str, command: GroupUpdateCommand):
        try:
            group = Group.model_validate(command)
            group.id = id
            group_updated = self.repo.update(id, group)
            if group_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return group_updated
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def delete(self, id: str) -> None:
        try:
            group = self.repo.delete(id)
            if group is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e

    def update_modules(self, id: str, command: list[str]) -> Group:
        modules = []
        for module_id in command:
            module = self.module_repo.read_by_id(module_id)
            if module is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=module_id))
            modules.append(module)
        group_updated = self.repo.update_modules(id, modules)
        if group_updated is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return group_updated

    def update_configuration_values(self, id: str, commands: list[ConfigurationValueCommand]) -> Group:
        group = self.read_by_id(id)
        group_updated = self.repo.upsert_configuration_value(commands, group)
        return group_updated
