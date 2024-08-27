from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.domain.models import Module, ModuleCommand, ModuleFilter
from src.app.modules.core.persistence.module_repo import ModuleRepo
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.configuration.lang import tr
from src.app.modules.core.utils.paginator import PageParams


class ModuleService:

    def __init__(self, repo: Annotated[ModuleRepo, Depends()], locale: Locale) -> None:
        self.repo = repo
        self.locale = locale

    def create(self, command: ModuleCommand) -> Module:
        try:
            module = Module.model_validate(command)
            return self.repo.create(module)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def read_by_id(self, id: str) -> Module:
        module = self.repo.read_by_id(id)
        if module is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return module

    def read_all(self) -> list[Module]:
        modules = self.repo.read_all()
        return modules

    def read_all_paginated(self, page_params: PageParams, filter: ModuleFilter) -> tuple[list[Module], int]:
        total = self.repo.count_all_filtered(filter)
        modules = self.repo.read_paginated(page_params, filter)
        return (modules, total)

    def update(self, id: str, command: ModuleCommand):
        try:
            module = Module.model_validate(command)
            module.id = id
            module_updated = self.repo.update(id, module)
            if module_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return module_updated
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.code)
            raise e

    def delete(self, id: str) -> None:
        try:
            module = self.repo.delete(id)
            if module is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e
