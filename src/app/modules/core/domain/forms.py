from typing import Generic, Type, TypeVar
from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from pydantic_core import ValidationError
from sqlmodel import SQLModel

from src.app.configuration.lang import tr

T = TypeVar("T", bound=SQLModel)


class Form(Generic[T]):
    def __init__(self, request: Request, model_type: Type[T] = None):
        self.model_type = model_type
        self.request: Request = request
        self.errors: dict[str, str] = {}

    async def load(self) -> None:
        await self.request.form()
        return self.to_dict()

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k not in ["request", "model_type", "self_path", "errors"]}

    def flash_message(self, msg: str, type: str) -> None:
        self.__flash(message={"msg": msg, "type": type})

    def flash_validation_errors(self, errors: dict) -> None:
        self.__flash(errors=errors)

    def flash_form_values(self, values: dict) -> None:
        self.__flash(form_values=values)

    def unflash(self):
        print(self.request.session)
        flash_keys = [k for k in self.request.session if "flash_" in k]
        for k in flash_keys:
            self.request.session.pop(k)

    @staticmethod
    def unflash_message(request: Request) -> dict[str, str]:
        return request.session.pop("flash_message", None)

    @staticmethod
    def unflash_validation_errors(request: Request) -> dict[str, str]:
        return request.session.pop("flash_errors", None)

    @staticmethod
    def unflash_form_values(request: Request) -> dict[str, str]:
        return request.session.pop("flash_form_values", None)

    @staticmethod
    def unflash_all(request: Request) -> dict[str, any]:
        message = Form.unflash_message(request)
        errors = Form.unflash_validation_errors(request)
        values = Form.unflash_form_values(request)
        has_error = True if errors or (message and message["type"]) == "danger" else False
        return {"f_message": message, "f_errors": errors, "f_values": values, "f_has_error": has_error}

    async def perform_validation(
        self, method_nok: str, method_nok_params: dict
    ) -> tuple[SQLModel, dict[str, str], Response]:
        command = None
        errors_dict = {}
        response = None
        try:
            if self.model_type is not None:
                command = self.model_type.model_validate(await self.load())
        except ValidationError as exc:
            errors = tr.t_errors(exc.errors(), self.request.state.locale)
            for error in errors:
                errors_dict[error["loc"][0]] = error["msg"]
            self.flash_validation_errors(errors_dict)
            self.flash_form_values(self.to_dict())
            redirect_ulr = self.request.url_for(method_nok, **method_nok_params)
            response = RedirectResponse(redirect_ulr, 303)
        return (command, errors_dict, response)

    async def perform_action(
        self, func: callable, method_ok: str, method_ok_params: dict, method_nok: str, method_nok_params: dict
    ) -> Response:
        try:
            func()
            redirect_ulr = self.request.url_for(method_ok, **method_ok_params)
            self.flash_message(tr.t("Successful operation", self.request.state.locale), "success")
        except Exception as e:
            redirect_ulr = self.request.url_for(method_nok, **method_nok_params)
            self.flash_message(tr.t(e.msg, self.request.state.locale) if e.msg else None, "danger")
            self.flash_form_values(self.to_dict())
        return RedirectResponse(redirect_ulr, 303)

    def __flash(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.request.session["flash_" + k] = v


""" Auth """


class LoginForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
        self.username = str
        self.password = str

    async def load(self) -> dict:
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")
        return self.to_dict()


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
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()


""" User """


class UserCreateForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
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
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
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


""" Module """


class ModuleForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        return self.to_dict()


""" Resource """


class ResourceForm(Form):
    def __init__(self, request: Request, model_type: Type[T]):
        super().__init__(request, model_type)
        self.code: str | None = None
        self.module_id: str | None = None

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.module_id = form.get("module_id")
        return self.to_dict()
