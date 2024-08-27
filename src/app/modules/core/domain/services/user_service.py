from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.dependencies import Locale
from src.app.modules.core.utils.exceptions import (
    EntityAlreadyExistsError,
    EntityNotFoundError,
    EntityRelationshipExistsError,
)
from src.app.modules.core.domain.models import User, UserCreateCommand, UserFilter, UserUpdateCommand
from src.app.modules.core.persistence.group_repo import GroupRepo
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.persistence.user_repo import UserRepo
from src.app.modules.core.utils.crypto import get_password_hash
from src.app.modules.core.utils.paginator import PageParams
from src.app.configuration.lang import tr


class UserService:

    def __init__(
        self,
        repo: Annotated[UserRepo, Depends()],
        role_repo: Annotated[RoleRepo, Depends()],
        group_repo: Annotated[GroupRepo, Depends()],
        locale: Locale,
    ) -> None:
        self.repo = repo
        self.role_repo = role_repo
        self.group_repo = group_repo
        self.locale = locale

    def create(self, command: UserCreateCommand) -> User:
        try:
            self.__validate(command)
            user = User.model_validate(command, update={"password": get_password_hash(command.password_raw)})
            return self.repo.create(user)
        except EntityAlreadyExistsError as e:
            e.msg = tr.t("Already exists", self.locale, entity=command.username)
            raise e

    def read_by_id(self, id: str) -> User:
        user = self.repo.read_by_id(id)
        if user is None:
            raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        return user

    def read_all(self) -> list[User]:
        users = self.repo.read_all()
        return users

    def read_all_paginated(self, page_params: PageParams, filter: UserFilter) -> tuple[list[User], int]:
        total = self.repo.count_all()
        users = self.repo.read_paginated(page_params, filter)
        return (users, total)

    def update(self, id: str, command: UserUpdateCommand):
        try:
            self.__validate(command)
            password = get_password_hash(command.password_raw) if (command.password_raw) else "nopass"
            user = User.model_validate(command, update={"password": password})
            user.id = id
            user_updated = self.repo.update(id, user)
            if user_updated is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
            return user_updated
        except EntityAlreadyExistsError as e:
            e.msg = "User code already exists"
            raise e

    def delete(self, id: str) -> None:
        try:
            user = self.repo.delete(id)
            if user is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=id))
        except EntityRelationshipExistsError as e:
            e.msg = tr.t("Entity has dependants", self.locale)
            raise e

    def __validate(self, command) -> None:
        if command.role_id:
            role = self.role_repo.read_by_id(command.role_id)
            if role is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.role_id))
        if command.group_id:
            group = self.group_repo.read_by_id(command.group_id)
            if group is None:
                raise EntityNotFoundError(msg=tr.t("Not found", self.locale, entity=command.group_id))
