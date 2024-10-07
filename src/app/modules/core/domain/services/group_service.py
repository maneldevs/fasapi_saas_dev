from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.persistence.configuration_repo import ConfigurationRepo
from src.app.modules.core.persistence.configuration_value_repo import ConfigurationValueRepo
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.modules.core.domain.models import (
    Configuration,
    ConfigurationValue,
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
        self,
        repo: Annotated[GroupRepo, Depends()],
        module_repo: Annotated[ModuleRepo, Depends()],
        configuration_repo: Annotated[ConfigurationRepo, Depends()],
        configuration_value_repo: Annotated[ConfigurationValueRepo, Depends()],
        locale: Locale,
    ) -> None:
        self.repo = repo
        self.module_repo = module_repo
        self.configuration_repo = configuration_repo
        self.configuration_value_repo = configuration_value_repo
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

    def read_configuration_values_index(self, id: str) -> list[ConfigurationValue]:
        group = self.read_by_id(id)
        return group.configuration_values

    def create_configuration_value(self, id: str, command: ConfigurationValueCommand) -> ConfigurationValue:
        try:
            group = self.read_by_id(id)
            configuration = self.__validate_configuration_value_command(command)
            configuration_value_dict = command.model_dump()
            configuration_value_dict.update({"configuration": configuration, "group": group})
            configuration_value = ConfigurationValue(**configuration_value_dict, group_id=id)
            configuration_value = ConfigurationValue.model_validate(configuration_value)
            return self.configuration_value_repo.create(configuration_value)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=f"g:{id} conf:{command.configuration_id}")
            raise e

    def __validate_configuration_value_command(self, command: ConfigurationValueCommand) -> Configuration:
        if command.configuration_id:
            configuration = self.configuration_repo.read_by_id(command.configuration_id)
            if configuration is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.configuration_id))
        return configuration or None
