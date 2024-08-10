from fastapi import Request


class GroupCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: dict[str, str] = {}
        self.code: str | None = None
        self.webname: str | None = None

    async def load(self):
        form = await self.request.form()
        self.code = form.get("code")
        self.webname = form.get("webname")

    def is_valid(self):
        valid = False
        if not self.code or len(self.code) == 0:
            self.errors["code"] = "code is required"
        if not self.webname or len(self.webname) == 0:
            self.errors["webname"] = "webname is required"
        if not self.errors or len(self.errors) == 0:
            valid = True
        return valid
