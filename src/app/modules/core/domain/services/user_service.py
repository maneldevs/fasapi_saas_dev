from typing import Annotated

from fastapi import Depends

from src.app.configuration.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.app.modules.core.domain.models import User, UserCreateCommand, UserFilter
from src.app.modules.core.persistence.group_repo import GroupRepo
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.persistence.user_repo import UserRepo
from src.app.modules.core.utils.crypto import get_password_hash
from src.app.modules.core.utils.paginator import PageParams


class UserService:

    def __init__(
        self,
        repo: Annotated[UserRepo, Depends()],
        role_repo: Annotated[RoleRepo, Depends()],
        group_repo: Annotated[GroupRepo, Depends()],
    ) -> None:
        self.repo = repo
        self.role_repo = role_repo
        self.group_repo = group_repo

    def create(self, command: UserCreateCommand) -> User:
        try:
            user = self.__validate_and_deserialize(command)
            return self.repo.create(user)
        except EntityAlreadyExistsError as e:
            e.msg = "User code already exists"
            raise e

    def read_all_paginated(self, page_params: PageParams, filter: UserFilter) -> tuple[list[User], int]:
        total = self.repo.count_all()
        users = self.repo.read_paginated(page_params, filter)
        return (users, total)

    def __validate_and_deserialize(self, command):
        if command.role_id:
            role = self.role_repo.read_by_id(command.role_id)
            if role is None:
                raise EntityNotFoundError(msg="Role not found")
        if command.group_id:
            group = self.group_repo.read_by_id(command.group_id)
            if group is None:
                raise EntityNotFoundError(msg="Group not found")
        user = User.model_validate(command, update={"password": get_password_hash(command.password_raw)})
        return user
