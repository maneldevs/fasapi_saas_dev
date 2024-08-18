from typing import Annotated

from fastapi import Depends

from src.app.modules.core.domain.models import EntitiesCountResponse
from src.app.modules.core.persistence.group_repo import GroupRepo
from src.app.modules.core.persistence.role_repo import RoleRepo
from src.app.modules.core.persistence.user_repo import UserRepo


class StatisticsService:

    def __init__(
        self,
        group_repo: Annotated[GroupRepo, Depends()],
        role_repo: Annotated[RoleRepo, Depends()],
        user_repo: Annotated[UserRepo, Depends()],
    ) -> None:
        self.group_repo = group_repo
        self.role_repo = role_repo
        self.user_repo = user_repo

    def counts(self) -> EntitiesCountResponse:
        group_count = self.group_repo.count_all()
        role_count = self.role_repo.count_all()
        user_count = self.user_repo.count_all()
        module_count = 0  # TODO mmr
        return EntitiesCountResponse(
            group_count=group_count, role_count=role_count, user_count=user_count, module_count=module_count
        )
