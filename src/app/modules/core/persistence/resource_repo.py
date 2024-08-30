from typing import Annotated
import uuid

from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from sqlmodel import Session

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import Module, Resource
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class ResourceRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_by_id(self, id: str) -> Module:
        resource = self.session.get(Resource, id)
        return resource

    def read_all_by_module(self, module: Module) -> list[Resource]:
        resources = module.resources
        return resources

    def create(self, resource: Resource) -> Resource:
        resource.id = str(uuid.uuid4())
        return self.__save(resource)

    def update(self, id: str, resource: Resource):
        resource_in_db = self.read_by_id(id)
        if resource_in_db is not None:
            resource_in_db.sqlmodel_update(resource)
            self.__save(resource_in_db)
        return resource_in_db

    def delete(self, id: str) -> Resource:
        resource_in_db = self.read_by_id(id)
        if resource_in_db is not None:
            self.__delete(resource_in_db)
        return resource_in_db

    def __save(self, resource: Resource) -> Resource:
        try:
            self.session.add(resource)
            self.session.commit()
            self.session.refresh(resource)
            return resource
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __delete(self, module):
        try:
            self.session.delete(module)
            self.session.commit()
        except IntegrityError as e:
            raise EntityRelationshipExistsError(original_exception=e)
