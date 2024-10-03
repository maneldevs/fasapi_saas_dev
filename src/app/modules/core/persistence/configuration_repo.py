from typing import Annotated
import uuid
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.app.modules.core.domain.models import Configuration
from src.app.configuration.database import get_session
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class ConfigurationRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_all(self) -> list[Configuration]:
        stmt = select(Configuration).order_by("code")
        configurations = self.session.exec(stmt).all()
        return configurations

    def read_by_id(self, id: str) -> Configuration:
        configuration = self.session.get(Configuration, id)
        return configuration

    def create(self, configuration: Configuration) -> Configuration:
        configuration.id = str(uuid.uuid4())
        return self.__save(configuration)

    def update(self, id: str, configuration: Configuration) -> Configuration:
        configuration_in_db = self.read_by_id(id)
        if configuration_in_db is not None:
            configuration_in_db.sqlmodel_update(configuration)
            self.__save(configuration_in_db)
        return configuration_in_db

    def delete(self, id: str) -> Configuration:
        configuration = self.read_by_id(id)
        if configuration is not None:
            self.__delete(configuration)
        return configuration

    def __save(self, configuration: Configuration) -> Configuration:
        try:
            self.session.add(configuration)
            self.session.commit()
            self.session.refresh(configuration)
            return configuration
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __delete(self, configuration: Configuration) -> None:
        try:
            self.session.delete(configuration)
            self.session.commit()
        except IntegrityError as e:
            raise EntityRelationshipExistsError(original_exception=e)
