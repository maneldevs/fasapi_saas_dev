from fastapi import Request


class Form:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict[str, str] = {}

    async def load(self) -> None:
        pass

    def is_valid(self) -> bool:
        pass

    def to_dict(self) -> dict:
        return self.__dict__


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
