from typing import Generic, Type, TypeVar
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError
from sqlmodel import SQLModel

from src.app import main
from src.app.configuration.lang import tr

T = TypeVar("T", bound=SQLModel)


# TODO mmr Refactorizar: 
    # borrar is_valid
    # refactorizar perform operation method en dos métodos y llamarlos de manera separada desde el controller (descomentarlos líneas 35 a 62)
    # pasar los params desde el controller (que serán el id (si no es create y el command que lo habrá obtenido el controller de la validación (1er método separado)

class Form(Generic[T]):
    def __init__(self, request: Request, model_type: Type[T], self_path: str = ""):
        self.model_type = model_type
        self.self_path = self_path
        self.request: Request = request
        self.errors: dict[str, str] = {}

    async def load(self) -> None:
        await self.request.form()
        return self.to_dict()

    async def is_valid(self):
        pass

    def to_dict(self) -> dict:
        return self.__dict__

    # async def validate(self, extra_context={}) -> tuple[SQLModel, dict[str, str], Response, dict]:
    #     context = await self.load()
    #     context |= extra_context
    #     errors_dict = {}
    #     try:
    #         if self.model_type is not None:
    #             command = self.model_type.model_validate(await self.load())
    #     except ValidationError as exc:
    #         errors = exc.errors()
    #         for error in errors:
    #             errors_dict[error["loc"][0]] = tr.t(error["msg"], self.request.state.locale)
    #             context |= {'errors': errors_dict}
    #     return (command, errors_dict, self.generate_error_response(self.request, self.self_path, context), context)

    # async def perform_operation(self, func: callable, params: dict, redirect_method_name, context={}) -> Response:
    #     try:
    #         func(**params)
    #         redirect_ulr = self.request.url_for(redirect_method_name).include_query_params(
    #             msg=tr.t("Successful operation", self.request.state.locale)
    #         )
    #         return RedirectResponse(redirect_ulr, 303)
    #     except Exception as e:
    #         context |= {"msg": e.msg, "type": "danger"}
    #     return self.generate_error_response(self.self_path, context)

    # def generate_error_response(self, request: Request, path: str, context: dict) -> Response:
    #     return main.templates.TemplateResponse(self.request, name=path, context=context)

    async def perform_operation(self, func, self_template_path, redirect_method_name, extra_context={}):
        context = await self.load()
        context |= extra_context
        my_errors = {}
        command = None
        # TODO mmr Separar (1er método que validará y devolverá command y si no valida devuelve el template?)
        try:
            if self.model_type is not None:
                command = self.model_type.model_validate(await self.load())
        except ValidationError as exc:
            errors = exc.errors()
            for error in errors:
                my_errors[error["loc"][0]] = tr.t(error["msg"], self.request.state.locale)
            context |= {'errors': my_errors}
            return main.templates.TemplateResponse(request=self.request, name=self_template_path, context=context)
        # TODO mmr Separar (2o método que llamará a la operación (los params vendrán del controller))
        if "id" in context and command:
            params = {"id": context["id"], "command": command}
        elif "id" in context:
            params = {"id": context["id"]}
        else:
            params = {"command": command}
        try:
            func(**params)
            redirect_ulr = self.request.url_for(redirect_method_name).include_query_params(
                msg=tr.t("Successful operation", self.request.state.locale)
            )
            return RedirectResponse(redirect_ulr, 303)
        except Exception as e:
            context |= {"msg": e.msg, "type": "danger"}
        return main.templates.TemplateResponse(request=self.request, name=self_template_path, context=context)


""" Auth """


class LoginForm(Form):
    def __init__(self, request: Request):
        super().__init__(request)
        self.username = str
        self.password = str

    async def load(self) -> dict:
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        return self.to_dict()

    def is_valid(self) -> bool:
        valid = False
        if not self.username or len(self.username) == 0:
            self.errors["username"] = tr.t("username is required", self.request.state.locale)
        if not self.password or len(self.password) == 0:
            self.errors["password"] = tr.t("password is required", self.request.state.locale)
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


""" Group """


class GroupCreateForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()


class GroupUpdateForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
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
    def __init__(self, request: Request):
        super().__init__(request)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()

    def is_valid(self) -> bool:
        valid = False
        if not self.code or len(self.code) == 0:
            self.errors["code"] = (
                tr.t("code", self.request.state.locale) + " " + tr.t("is required", self.request.state.locale)
            )
        if not self.webname or len(self.webname) == 0:
            self.errors["webname"] = (
                tr.t("webname", self.request.state.locale) + " " + tr.t("is required", self.request.state.locale)
            )
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


""" User """


class UserCreateForm(Form):
    def __init__(self, request: Request):
        super().__init__(request)
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

    def is_valid(self) -> bool:
        valid = False
        if not self.username or len(self.username) == 0:
            self.errors["username"] = (
                tr.t("username", self.request.state.locale) + " " + tr.t("is required", self.request.state.locale)
            )
        if not self.password_raw or len(self.password_raw) == 0:
            self.errors["password_raw"] = (
                tr.t("password", self.request.state.locale) + " " + tr.t("is required", self.request.state.locale)
            )
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


class UserUpdateForm(Form):
    def __init__(self, request: Request):
        super().__init__(request)
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

    def is_valid(self) -> bool:
        valid = False
        if not self.username or len(self.username) == 0:
            self.errors["username"] = (
                tr.t("username", self.request.state.locale) + " " + tr.t("is required", self.request.state.locale)
            )
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid
