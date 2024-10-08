from typing import Annotated
from fastapi import Depends
from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import Resource, ResourceUpdateCommand
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.persistence.resource_repo import ResourceRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.configuration.lang import tr


class ResourceService:

    def __init__(
        self, repo: Annotated[ResourceRepo, Depends()], module_repo: Annotated[ModuleRepo, Depends()], locale: Locale
    ) -> None:
        self.repo = repo
        self.module_repo = module_repo
        self.locale = locale

    def read_by_id(self, id: str) -> Resource:
        resource = self.repo.read_by_id(id)
        if resource is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return resource

    def update(self, id: str, command: ResourceUpdateCommand):
        try:
            self.__validate(command)
            resource = Resource.model_validate(command, update={"id": id})
            resource_updated = self.repo.update(id, resource)
            if resource_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return resource_updated
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def delete(self, id: str):
        try:
            resource = self.repo.delete(id)
            if resource is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e

    def __validate(self, command: ResourceUpdateCommand) -> None:
        if command.module_id:
            module = self.module_repo.read_by_id(command.module_id)
            if module is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.module_id))
