from typing import Annotated
import uuid

from fastapi import Depends
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import ConfigurationValue
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class ConfigurationValueRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_by_id(self, id: str):
        configuration_value = self.session.get(ConfigurationValue, id)
        return configuration_value

    def create(self, configuration_value: ConfigurationValue) -> ConfigurationValue:
        configuration_value.id = str(uuid.uuid4())
        return self.__save(configuration_value)

    def update(self, id: str, configuration_value: ConfigurationValue):
        configuration_value_in_db = self.read_by_id(id)
        configuration_value.group_id = configuration_value_in_db.group_id
        configuration_value.configuration_id = configuration_value_in_db.configuration_id
        if configuration_value_in_db is not None:
            configuration_value_in_db.sqlmodel_update(configuration_value)
            self.__save(configuration_value_in_db)
        return configuration_value_in_db

    def delete(self, id: str) -> ConfigurationValue:
        configuration_value_in_db = self.read_by_id(id)
        if configuration_value_in_db is not None:
            self.__delete(configuration_value_in_db)
        return configuration_value_in_db

    def __save(self, configuration_value: ConfigurationValue) -> ConfigurationValue:
        try:
            self.session.add(configuration_value)
            self.session.commit()
            self.session.refresh(configuration_value)
            return configuration_value
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __delete(self, configuration_value: ConfigurationValue):
        try:
            self.session.delete(configuration_value)
            self.session.commit()
        except IntegrityError as e:
            raise EntityRelationshipExistsError(original_exception=e)
