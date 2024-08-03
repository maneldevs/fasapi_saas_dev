from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.configuration.exceptions import EntityAlreadyExistsError
from src.app.modules.core.domain.group_models import Group


class GroupRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def create(self, group: Group) -> Group:
        try:
            self.session.add(group)
            self.session.commit()
            self.session.refresh(group)
            return group
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)
