from datetime import timedelta
from typing import Annotated

from fastapi import Depends

from src.app.configuration.settings import settings
from src.app.modules.core.utils.exceptions import CredentialsError
from src.app.modules.core.domain.models import Login, LoginCommand, User
from src.app.modules.core.persistence.user_repo import UserRepo
from src.app.modules.core.utils.crypto import create_access_token, verify_password


class AuthService:

    def __init__(self, user_repo: Annotated[UserRepo, Depends()]) -> None:
        self.user_repo = user_repo

    def authenticate(self, command: LoginCommand) -> Login:
        self.__verify_credentials(command)
        return self.__generate_access_token(command.username)

    def __verify_credentials(self, command: LoginCommand) -> User:
        user = self.user_repo.read_by_username(command.username)
        if not user or not user.active or not verify_password(command.password, user.password):
            raise CredentialsError("Invalid credentials")

    def __generate_access_token(self, username: str) -> str:
        data = {"sub": username}
        exp_min = timedelta(minutes=settings.access_token_expire_minutes)
        token = create_access_token(data, settings.secret_key, settings.algorithm, exp_min)
        return Login(access_token=token)
