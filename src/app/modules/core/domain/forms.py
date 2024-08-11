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

    async def perform_operation(self, func, params, self_template_path, redirect_method_name):
        form_data = await self.load()
        if self.is_valid():
            try:
                func(**params)
                redirect_ulr = self.request.url_for(redirect_method_name).include_query_params(
                    msg="Successful operation"
                )
                return RedirectResponse(redirect_ulr, 303)
            except Exception as e:
                form_data |= {"msg": e.msg, "type": "danger"}
        return main.templates.TemplateResponse(request=self.request, name=self_template_path, context=form_data)


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
