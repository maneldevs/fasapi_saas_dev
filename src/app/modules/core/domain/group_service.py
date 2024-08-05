from typing import Annotated

from fastapi import Depends

from src.app.configuration.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.app.modules.core.domain.group_models import Group, GroupCreateCommand
from src.app.modules.core.persistence.group_repo import GroupRepo


class GroupService:

    def __init__(self, repo: Annotated[GroupRepo, Depends()]) -> None:
        self.repo = repo

    def create(self, command: GroupCreateCommand):
        try:
            group = Group.model_validate(command)
            return self.repo.create(group)
        except EntityAlreadyExistsError as e:
            e.msg = "Group already exists"
            raise e

    def read_by_id(self, id: str):
        group = self.repo.read_by_id(id)
        if group is None:
            raise EntityNotFoundError(msg="Group not found")
        return group
