from typing import Annotated
from fastapi import Depends
from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import Menu, MenuCommand
from src.app.modules.core.persistence.menu_repo import MenuRepo
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.configuration.lang import tr


class MenuService:

    def __init__(
        self, repo: Annotated[MenuRepo, Depends()], module_repo: Annotated[ModuleRepo, Depends()], locale: Locale
    ) -> None:
        self.repo = repo
        self.module_repo = module_repo
        self.locale = locale

    def read_all_root(self):
        menus = self.repo.read_all_root()
        return menus

    def read_by_id(self, id: str) -> Menu:
        menu = self.repo.read_by_id(id)
        if menu is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return menu

    def create(self, command: MenuCommand) -> Menu:
        try:
            self.__validate(command)
            menu = Menu.model_validate(command)
            return self.repo.create(menu)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def update(self, id: str, command: MenuCommand):
        try:
            self.__validate(command)
            menu = Menu.model_validate(command)
            menu.id = id
            menu_updated = self.repo.update(id, menu)
            if menu_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return menu_updated
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def delete(self, id: str) -> None:
        try:
            menu = self.repo.delete(id)
            if menu is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e

    def __validate(self, command: MenuCommand) -> None:
        if command.module_id:
            module = self.module_repo.read_by_id(command.module_id)
            if module is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.module_id))
        if command.parent_id:
            self.read_by_id(command.parent_id)
