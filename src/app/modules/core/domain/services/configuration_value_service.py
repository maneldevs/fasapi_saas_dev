from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import ConfigurationValue, ConfigurationValueUpdateCommand
from src.app.modules.core.persistence.configuration_repo import ConfigurationRepo
from src.app.modules.core.persistence.configuration_value_repo import ConfigurationValueRepo
from src.app.modules.core.utils.exceptions import EntityNotFoundError, EntityRelationshipExistsError
from src.app.configuration.lang import tr


class ConfigurationValueService:
    def __init__(
        self,
        repo: Annotated[ConfigurationValueRepo, Depends()],
        config_repo: Annotated[ConfigurationRepo, Depends()],
        locale: Locale,
    ):
        self.repo = repo
        self.config_repo = config_repo
        self.locale = locale

    def read_by_id(self, id: str) -> ConfigurationValue:
        configuration_value = self.repo.read_by_id(id)
        if configuration_value is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return configuration_value

    def update(self, id: str, command: ConfigurationValueUpdateCommand) -> ConfigurationValue:
        configuration_value = ConfigurationValue(id=id, **command.model_dump(exclude_defaults=True))
        configuration_value.id = id
        configuration_value_updated = self.repo.update(id, configuration_value)
        if configuration_value_updated is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return configuration_value_updated

    def delete(self, id: str) -> None:
        try:
            configuration_value = self.repo.delete(id)
            if configuration_value is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e
