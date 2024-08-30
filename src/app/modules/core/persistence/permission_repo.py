from typing import Annotated
import uuid

from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from sqlmodel import Session

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import Permission, Role
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class PermissionRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_by_id(self, id: str) -> Permission:
        permission = self.session.get(Permission, id)
        return permission

    def read_all_by_role(self, role: Role) -> list[Permission]:
        permissions = role.permissions
        return permissions

    def create(self, permission: Permission) -> Permission:
        permission.id = str(uuid.uuid4())
        return self.__save(permission)

    def update(self, id: str, permission: Permission):
        permission_in_db = self.read_by_id(id)
        if permission_in_db is not None:
            permission_in_db.sqlmodel_update(permission)
            self.__save(permission_in_db)
        return permission_in_db

    def delete(self, id: str) -> Permission:
        permission_in_db = self.read_by_id(id)
        if permission_in_db is not None:
            self.__delete(permission_in_db)
        return permission_in_db

    def __save(self, permission: Permission) -> Permission:
        try:
            self.session.add(permission)
            self.session.commit()
            self.session.refresh(permission)
            return permission
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __delete(self, permission: Permission):
        try:
            self.session.delete(permission)
            self.session.commit()
        except IntegrityError as e:
            raise EntityRelationshipExistsError(original_exception=e)
