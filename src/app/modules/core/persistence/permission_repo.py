from typing import Annotated
import uuid

from sqlalchemy.exc import IntegrityError
from fastapi import Depends
from sqlmodel import Session, select

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import Permission, PermissionFilter, Resource, Role
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class PermissionRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_by_id(self, id: str) -> Permission:
        permission = self.session.get(Permission, id)
        return permission

    def read_all_by_role(self, role: Role, filter: PermissionFilter = None) -> list[Permission]:
        stmt = select(Permission).join(Resource)
        if filter and filter.module_id:
            stmt = stmt.where(Permission.role_id == role.id)
            stmt = stmt.where(Resource.module_id == filter.module_id)
        permissions = self.session.exec(stmt).all()
        for p in permissions:
            self.session.refresh(p)
        return permissions

    def create(self, permission: Permission) -> Permission:
        permission.id = str(uuid.uuid4())
        return self.__save(permission)

    def update(self, id: str, permission: Permission):
        permission_in_db = self.read_by_id(id)
        permission_dict = permission.model_dump(exclude=["role_id", "resource_id"])
        if permission_in_db is not None:
            permission_in_db.sqlmodel_update(permission_dict)
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
