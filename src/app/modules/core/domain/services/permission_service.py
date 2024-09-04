from typing import Annotated

from fastapi import Depends
from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import Permission, PermissionUpdateCommand
from src.app.modules.core.persistence.permission_repo import PermissionRepo
from src.app.modules.core.utils.exceptions import EntityNotFoundError, EntityRelationshipExistsError
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

    def update(self, id: str, command: PermissionUpdateCommand):
        permission = Permission(id=id, **command.model_dump())
        permission_updated = self.repo.update(id, permission)
        if permission_updated is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return permission_updated

    def delete(self, id: str):
        try:
            permission = self.repo.delete(id)
            if permission is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e
