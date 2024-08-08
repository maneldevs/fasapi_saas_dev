from typing import Annotated
import uuid
from fastapi import Depends
from sqlmodel import Session, select, func, col, or_
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.configuration.exceptions import EntityAlreadyExistsError
from src.app.modules.core.domain.models import Role, RoleFilter
from src.app.modules.core.utils.paginator import Paginator
from src.app.modules.core.utils.paginator import PageParams


class RoleRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def __save(self, role: Role) -> Role:
        try:
            self.session.add(role)
            self.session.commit()
            self.session.refresh(role)
            return role
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def read_by_id(self, id: str) -> Role:
        role = self.session.get(Role, id)
        return role

    def read_all(self) -> list[Role]:
        stmt = select(Role)
        roles = self.session.exec(stmt).all()
        return roles

    def count_all(self) -> int:
        stmt = select(func.count(col(Role.id)))
        total = self.session.exec(stmt).one()
        return total

    def read_paginated(self, page_params: PageParams, filter: RoleFilter):
        stmt = select(Role)
        if filter.target:
            stmt = stmt.where(or_(col(Role.code).contains(filter.target), col(Role.webname).contains(filter.target)))
        stmt = Paginator(Role).paginate_query(stmt, page_params)
        roles = self.session.exec(stmt).all()
        return roles

    def create(self, role: Role) -> Role:
        role.id = str(uuid.uuid4())
        return self.__save(role)

    def update(self, id: str, role: Role):
        role_in_db = self.read_by_id(id)
        if (role_in_db is not None):
            role_in_db.sqlmodel_update(role)
            self.__save(role_in_db)
        return role_in_db

    def delete(self, id: str) -> Role:
        role_in_db = self.read_by_id(id)
        if (role_in_db is not None):
            self.session.delete(role_in_db)
            self.session.commit()
        return role_in_db
