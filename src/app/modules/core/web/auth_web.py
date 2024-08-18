from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from src.app import main
from src.app.modules.core.domain.forms import LoginForm
from src.app.modules.core.domain.models import LoginCommand
from src.app.modules.core.domain.services.auth_service import AuthService

router = APIRouter(prefix="/core/auth")


@router.get("/", response_class=HTMLResponse)
async def admin_login(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/login.html", context={})


@router.post("/", response_class=HTMLResponse)
async def admin_login_perform(request: Request, service: Annotated[AuthService, Depends()]):
    form = LoginForm(request)
    context = await form.load()
    if form.is_valid():
        try:
            command = LoginCommand.model_validate(context)
            token = service.authenticate(command)
            redirect_ulr = request.url_for("group_list").include_query_params(msg="Successful operation")
            response = RedirectResponse(redirect_ulr, 303)
            response.set_cookie("token", token.access_token, httponly=True)
            return response
        except Exception as e:
            context |= {"msg": e.msg, "type": "danger"}
    return main.templates.TemplateResponse(request=request, name="core/login.html", context=context)


@router.get("/logout")
async def admin_logout(request: Request):
    redirect_ulr = request.url_for("admin_login")
    response = RedirectResponse(redirect_ulr, 303)
    response.delete_cookie("token")
    return response
