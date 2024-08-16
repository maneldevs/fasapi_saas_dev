from fastapi import Request
from fastapi.responses import RedirectResponse

from src.app import main


class Form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict[str, str] = {}

    async def load(self) -> None:
        await self.request.form()
        return self.to_dict()

    def is_valid(self) -> bool:
        return True

    def to_dict(self) -> dict:
        return self.__dict__

    async def perform_operation(self, func, params, self_template_path, redirect_method_name, extra_context={}):
        context = await self.load()
        context |= extra_context
        if self.is_valid():
            try:
                func(**params)
                redirect_ulr = self.request.url_for(redirect_method_name).include_query_params(
                    msg="Successful operation"
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
            self.errors["username"] = "username is required"
        if not self.password or len(self.password) == 0:
            self.errors["password"] = "password is required"
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


""" Group """


class GroupCreateForm(Form):
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
            self.errors["code"] = "code is required"
        if not self.webname or len(self.webname) == 0:
            self.errors["webname"] = "webname is required"
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


class GroupUpdateForm(Form):
    def __init__(self, request: Request):
        super().__init__(request)
        self.code: str | None = None
        self.webname: str | None = None
        self.active: bool

    async def load(self) -> dict:
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")
        self.active = form.get("active") if form.get("active") else False
        return self.to_dict()

    def is_valid(self) -> bool:
        valid = False
        if not self.code or len(self.code) == 0:
            self.errors["code"] = "code is required"
        if not self.webname or len(self.webname) == 0:
            self.errors["webname"] = "webname is required"
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid


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
            self.errors["code"] = "code is required"
        if not self.webname or len(self.webname) == 0:
            self.errors["webname"] = "webname is required"
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
            self.errors["username"] = "username is required"
        if not self.password_raw or len(self.password_raw) == 0:
            self.errors["password_raw"] = "password is required"
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
            self.errors["username"] = "username is required"
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid
