from typing import Annotated
import uuid

from fastapi import Depends
from sqlmodel import Session, select
from sqlalchemy.sql.operators import is_
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.modules.core.domain.models import Menu
from src.app.modules.core.utils.exceptions import EntityAlreadyExistsError, EntityRelationshipExistsError


class MenuRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def read_all_root(self):
        stmt = select(Menu).where(is_(Menu.parent_id, None))
        menus = self.session.exec(stmt).all()
        return menus

    def read_by_id(self, id: str) -> Menu:
        menu = self.session.get(Menu, id)
        return menu

    def create(self, menu: Menu) -> Menu:
        menu.id = str(uuid.uuid4())
        return self.__save(menu)

    def update(self, id: str, menu: Menu):
        menu_in_db = self.read_by_id(id)
        if (menu_in_db is not None):
            menu_in_db.sqlmodel_update(menu)
            self.__save(menu_in_db)
        return menu_in_db

    def delete(self, id: str) -> Menu:
        menu_in_db = self.read_by_id(id)
        if (menu_in_db is not None):
            self.__delete(menu_in_db)
        return menu_in_db

    def __save(self, menu: Menu) -> Menu:
        try:
            self.session.add(menu)
            self.session.commit()
            self.session.refresh(menu)
            return menu
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def __delete(self, menu: Menu):
        try:
            self.session.delete(menu)
            self.session.commit()
        except IntegrityError as e:
            raise EntityRelationshipExistsError(original_exception=e)
