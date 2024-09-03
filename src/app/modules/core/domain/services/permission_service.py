from typing import Annotated

from fastapi import Depends
from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import Permission
from src.app.modules.core.persistence.permission_repo import PermissionRepo
from src.app.modules.core.utils.exceptions import EntityNotFoundError
from src.app.configuration.lang import tr


class PermissionService:

    def __init__(self, repo: Annotated[PermissionRepo, Depends()], locale: Locale) -> None:
        self.repo = repo
        self.locale = locale

    def read_by_id(self, id: str) -> Permission:
        permission = self.repo.read_by_id(id)
        if permission is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return permission

    # def update(self, id: str, command: ResourceUpdateCommand):
    #     try:
    #         self.__validate(command)
    #         resource = Resource.model_validate(command, update={"id": id})
    #         resource_updated = self.repo.update(id, resource)
    #         if resource_updated is None:
    #             raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
    #         return resource_updated
    #     except EntityAlreadyExistsError as e:
    #         e.msg = tr.t("Already exists", self.locale, entity=command.code)
    #         raise e

    # def delete(self, id: str):
    #     try:
    #         resource = self.repo.delete(id)
    #         if resource is None:
    #             raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
    #     except EntityRelationshipExistsError as e:
    #         e.msg = tr.t("Entity has dependants", self.locale)
    #         raise e

    # def __validate(self, command: ResourceUpdateCommand) -> None:
    #     if command.module_id:
    #         role = self.module_repo.read_by_id(command.module_id)
    #         if role is None:
    #             raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.module_id))