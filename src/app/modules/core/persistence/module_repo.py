from typing import Annotated
import uuid

from fastapi import Depends
from sqlmodel import Session, select, func, col, or_
from sqlmodel.sql.expression import SelectOfScalar
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import Module, ModuleFilter
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError
from src.app.modules.core.utils.paginator import PageParams, Paginator


class ModuleRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def __save(self, module: Module) -> Module:
        try:
            self.session.add(module)
            self.session.commit()
            self.session.refresh(module)
            return module
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def read_by_id(self, id: str) -> Module:
        module = self.session.get(Module, id)
        return module

    def read_all(self) -> list[Module]:
        stmt = select(Module)
        modules = self.session.exec(stmt).all()
        return modules

    def count_all(self) -> int:
        stmt = select(func.count(col(Module.id)))
        total = self.session.exec(stmt).one()
        return total

    def count_all_filtered(self, filter: ModuleFilter) -> int:
        stmt = select(func.count(col(Module.id)))
        stmt = self.__apply_filter(stmt, filter)
        total = self.session.exec(stmt).one()
        return total

    def read_paginated(self, page_params: PageParams, filter: ModuleFilter):
        stmt = select(Module)
        stmt = self.__apply_filter(stmt, filter)
        stmt = Paginator(Module).paginate_query(stmt, page_params)
        modules = self.session.exec(stmt).all()
        return modules

    def create(self, module: Module) -> Module:
        module.id = str(uuid.uuid4())
        return self.__save(module)

    def update(self, id: str, module: Module):
        module_in_db = self.read_by_id(id)
        if module_in_db is not None:
            module_in_db.sqlmodel_update(module)
            self.__save(module_in_db)
        return module_in_db

    def delete(self, id: str) -> Module:
        module_in_db = self.read_by_id(id)
        if module_in_db is not None:
            self.session.delete(module_in_db)
            self.session.commit()
        return module_in_db

    def __apply_filter(self, stmt: SelectOfScalar[Module], filter: ModuleFilter):
        if filter.target:
            stmt = stmt.where(
                or_(col(Module.code).contains(filter.target), col(Module.webname).contains(filter.target))
            )
        return stmt
