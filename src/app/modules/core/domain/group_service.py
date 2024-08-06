from typing import Annotated

from fastapi import Depends

from src.app.configuration.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.app.modules.core.domain.models import Group, GroupCreateCommand, GroupFilter, GroupUpdateCommand
from src.app.modules.core.persistence.group_repo import GroupRepo
from src.app.modules.core.utils.paginator import PageParams


class GroupService:

    def __init__(self, repo: Annotated[GroupRepo, Depends()]) -> None:
        self.repo = repo

    def create(self, command: GroupCreateCommand) -> Group:
        try:
            group = Group.model_validate(command)
            return self.repo.save(group)
        except EntityAlreadyExistsError as e:
            e.msg = "Group code already exists"
            raise e

    def read_by_id(self, id: str) -> Group:
        group = self.repo.read_by_id(id)
        if group is None:
            raise EntityNotFoundError(msg="Group not found")
        return group

    def read_all(self) -> list[Group]:
        groups = self.repo.read_all()
        return groups

    def read_all_paginated(self, page_params: PageParams, filter: GroupFilter) -> tuple[list[Group], int]:
        total = self.repo.count_all()
        groups = self.repo.read_paginated(page_params, filter)
        return (groups, total)

    def update(self, id: str, command: GroupUpdateCommand):
        try:
            group = Group.model_validate(command)
            group_updated = self.repo.update(id, group)
            if (group_updated is None):
                raise EntityNotFoundError(msg="Group not found")
            return group_updated
        except EntityAlreadyExistsError as e:
            e.msg = "Group code already exists"
            raise e

    def delete(self, id: str) -> None:
        group = self.repo.delete(id)
        if (group is None):
            raise EntityNotFoundError(msg="Group not found")
