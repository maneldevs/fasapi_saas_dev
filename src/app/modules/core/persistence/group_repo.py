from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, select, func, col, or_
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.configuration.exceptions import EntityAlreadyExistsError
from src.app.modules.core.domain.models import Group, GroupFilter
from src.app.modules.core.utils.paginator import Paginator
from src.app.modules.core.utils.paginator import PageParams


class GroupRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def __save(self, group: Group) -> Group:
        try:
            self.session.add(group)
            self.session.commit()
            self.session.refresh(group)
            return group
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def read_by_id(self, id: str) -> Group:
        group = self.session.get(Group, id)
        return group

    def read_all(self) -> list[Group]:
        stmt = select(Group)
        groups = self.session.exec(stmt).all()
        return groups

    def count_all(self) -> int:
        stmt = select(func.count(col(Group.id)))
        total = self.session.exec(stmt).one()
        return total

    def read_paginated(self, page_params: PageParams, filter: GroupFilter):
        stmt = select(Group)
        if filter.target:
            stmt = stmt.where(or_(col(Group.code).contains(filter.target), col(Group.webname).contains(filter.target)))
        stmt = Paginator(Group).paginate_query(stmt, page_params)
        groups = self.session.exec(stmt).all()
        return groups

    def create(self, group: Group) -> Group:
        return self.__save(group)

    def update(self, id: str, group: Group):
        group_in_db = self.read_by_id(id)
        if (group_in_db is not None):
            group_in_db.sqlmodel_update(group)
            self.__save(group_in_db)
        return group_in_db

    def delete(self, id: str) -> Group:
        group_in_db = self.read_by_id(id)
        if (group_in_db is not None):
            self.session.delete(group_in_db)
            self.session.commit()
        return group_in_db
