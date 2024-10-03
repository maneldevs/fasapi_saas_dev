from fastapi import Depends
from typing import Annotated
from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.persistence.configuration_repo import ConfigurationRepo
from src.app.modules.core.domain.models import Configuration, ConfigurationCommand
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.app.configuration.lang import tr


class ConfigurationService:
    def __init__(
        self,
        repo: Annotated[ConfigurationRepo, Depends()],
        module_repo: Annotated[ModuleRepo, Depends()],
        locale: Locale,
    ):
        self.repo = repo
        self.module_repo = module_repo
        self.locale = locale

    def create(self, command: ConfigurationCommand) -> Configuration:
        try:
            self.__validate(command)
            configuration = Configuration.model_validate(command)
            return self.repo.create(configuration)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def read_all(self) -> list[Configuration]:
        configurations = self.repo.read_all()
        return configurations

    def read_by_id(self, id: str) -> Configuration:
        configuration = self.repo.read_by_id(id)
        if configuration is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return configuration

    def update(self, id: str, command: ConfigurationCommand) -> Configuration:
        try:
            self.__validate(command)
            configuration = Configuration.model_validate(command)
            configuration.id = id
            configuration_updated = self.repo.update(id, configuration)
            if configuration_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return configuration_updated
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def delete(self, id: str) -> None:
        try:
            configuration = self.repo.delete(id)
            if configuration is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityNotFoundError as e:
            e.msg = tr.t("Not found", self.locale, entity=id)
            raise e

    def __validate(self, command: ConfigurationCommand) -> None:
        if command.module_id:
            module = self.module_repo.read_by_id(command.module_id)
            if module is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.module_id))

    # TODO: read_all_by_group read_by_id, create and update configuration values En este fichero o en otro?
