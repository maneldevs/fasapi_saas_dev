from typing import Annotated
import uuid

from fastapi import Depends
from sqlmodel import Session, or_, select, func, col
from sqlalchemy.exc import IntegrityError
from sqlmodel.sql.expression import SelectOfScalar

from src.app.configuration.database import get_session
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError
from src.app.modules.core.domain.models import User, UserFilter
from src.app.modules.core.utils.paginator import PageParams, Paginator


class UserRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def count_all(self) -> int:
        stmt = select(func.count(col(User.id)))
        total = self.session.exec(stmt).one()
        return total

    def count_all_paginated(self, filter: UserFilter) -> int:
        stmt = select(func.count(col(User.id)))
        stmt = self.__apply_filter(stmt, filter)
        total = self.session.exec(stmt).one()
        return total

    def read_by_id(self, id: str) -> User | None:
        user = self.session.get(User, id)
        return user

    def read_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.session.exec(stmt).first()

    def read_all(self) -> list[User]:
        stmt = select(User)
        users = self.session.exec(stmt).all()
        return users

    def read_paginated(self, page_params: PageParams, filter: UserFilter) -> list[User]:
        stmt = select(User)
        stmt = self.__apply_filter(stmt, filter)
        stmt = Paginator(User).paginate_query(stmt, page_params)
        users = self.session.exec(stmt).all()
        for user in users:
            self.session.refresh(user)
        return users

    def create(self, user: User) -> User:
        user.id = str(uuid.uuid4())
        return self.__save(user)

    def update(self, id: str, user: User):
        user_in_db = self.read_by_id(id)
        if user.password == "nopass":
            user.password = user_in_db.password
        if (user_in_db is not None):
            user_in_db.sqlmodel_update(user)
            self.__save(user_in_db)
        return user_in_db

    def delete(self, id: str) -> User:
        user_in_db = self.read_by_id(id)
        if (user_in_db is not None):
            self.session.delete(user_in_db)
            self.session.commit()
        return user_in_db

    def __save(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __apply_filter(self, stmt: SelectOfScalar[User], filter: UserFilter):
        if filter.target:
            stmt = stmt.where(
                or_(
                    col(User.username).contains(filter.target),
                    col(User.firstname).contains(filter.target),
                    col(User.lastname).contains(filter.target),
                )
            )
        if filter.active is not None:
            stmt = stmt.where(User.active == filter.active)
        if filter.is_god is not None:
            stmt = stmt.where(User.is_god == filter.is_god)
        if filter.group_id:
            stmt = stmt.where(User.group_id == filter.group_id)
        return stmt
