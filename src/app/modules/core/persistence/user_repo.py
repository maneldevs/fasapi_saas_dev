from typing import Annotated
import uuid

from fastapi import Depends
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from src.app.configuration.database import get_session
from src.app.configuration.exceptions import EntityAlreadyExistsError
from src.app.modules.core.domain.models import User


class UserRepo:

    def __init__(self, session: Annotated[Session, Depends(get_session)]) -> None:
        self.session = session

    def __save(self, user: User) -> User:
        try:
            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)
            return user
        except IntegrityError as e:
            raise EntityAlreadyExistsError(original_exception=e)

    def create(self, user: User) -> User:
        user.id = str(uuid.uuid4())
        return self.__save(user)
