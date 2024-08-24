from typing import Generic, Type, TypeVar
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError
from sqlmodel import SQLModel

from src.app import main
from src.app.configuration.lang import tr

T = TypeVar("T", bound=SQLModel)


class Form(Generic[T]):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        self.model_type = model_type
        self.self_path = self_path
        self.request: Request = request
        self.errors: dict[str, str] = {}

    async def load(self) -> None:
        await self.request.form()
        return self.to_dict()

    def to_dict(self) -> dict:
        return self.__dict__

    async def validate(self, extra_context={}) -> tuple[SQLModel, dict[str, str], Response, dict]:
        context = await self.load()
        context |= extra_context
        errors_dict = {}
        response = None
        command = None
        try:
            if self.model_type is not None:
                command = self.model_type.model_validate(await self.load())
        except ValidationError as exc:
            errors = exc.errors()
            for error in errors:
                errors_dict[error["loc"][0]] = tr.t(error["msg"], self.request.state.locale)
                context |= {'errors': errors_dict}
            response = self.generate_error_response(context)
        return (command, errors_dict, response, context)

    async def perform_operation(self, func: callable, params: dict, redirect_method_name, context={}) -> Response:
        try:
            func(**params)
            redirect_ulr = self.request.url_for(redirect_method_name).include_query_params(
                msg=tr.t("Successful operation", self.request.state.locale)
            )
            return RedirectResponse(redirect_ulr, 303)
        except Exception as e:
            context |= {"msg": e.msg, "type": "danger"}
        return self.generate_error_response(context)

    def generate_error_response(self, context: dict) -> Response:
        return main.templates.TemplateResponse(self.request, name=self.self_path, context=context)


""" Auth """


class LoginForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.username = str
        self.password = str

    async def load(self) -> dict:
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        return self.to_dict()


""" Group """


class GroupCreateForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()


class GroupUpdateForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.code: str | None = None
        self.webname: str | None = None
        self.active: bool

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        self.active = form.get("active") if form.get("active") else False
        return self.to_dict()


""" Role """


class RoleForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()


""" User """


class UserCreateForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.username: str
        self.password_raw: str
        self.firstname: str | None = None
        self.lastname: str | None = None
        self.group_id: str | None = None
        self.role_id: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.username = form.get("username")
        self.password_raw = form.get("password_raw")
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")
        self.group_id = form.get("group_id") if form.get("group_id") else None
        self.role_id = form.get("role_id") if form.get("role_id") else None
        return self.to_dict()


class UserUpdateForm(Form):
    def __init__(self, request: Request, model_type: Type[T], self_path: str):
        super().__init__(request, model_type, self_path)
        self.username: str
        self.password_raw: str | None
        self.firstname: str | None = None
        self.lastname: str | None = None
        self.group_id: str | None = None
        self.role_id: str | None = None
        self.active: bool
        self.is_god: bool

    async def load(self) -> dict:
        form = await self.request.form()
        self.username = form.get("username")
        self.password_raw = form.get("password_raw") if form.get("password_raw") else None
        self.firstname = form.get("firstname")
        self.lastname = form.get("lastname")
        self.group_id = form.get("group_id") if form.get("group_id") else None
        self.role_id = form.get("role_id") if form.get("role_id") else None
        self.active = form.get("active") if form.get("active") else False
        self.is_god = form.get("is_god") if form.get("is_god") else False
        return self.to_dict()
