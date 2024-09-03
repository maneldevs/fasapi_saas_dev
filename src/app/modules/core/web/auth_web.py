from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from src.app import main
from src.app.modules.core.domain.forms import LoginForm
from src.app.modules.core.domain.models import LoginCommand
from src.app.modules.core.domain.services.auth_service import AuthService
from src.app.configuration.lang import tr

router = APIRouter(prefix="/core/auth")


@router.get("/", response_class=HTMLResponse)
async def admin_login(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/login.html", context={})


@router.post("/", response_class=HTMLResponse)
async def admin_login_perform(request: Request, service: Annotated[AuthService, Depends()]):
    form = LoginForm(request, LoginCommand)
    command, errors_dict, response = await form.perform_validation("admin_login_perform", {})
    if errors_dict:
        return response
    try:
        token = service.authenticate(command)
        redirect_ulr = request.url_for("admin_index")
        form.flash_message(tr.t("Successful operation", request.state.locale), "success")
        response = RedirectResponse(redirect_ulr, 303)
        response.set_cookie("token", token.access_token, httponly=True)
    except Exception as e:
        redirect_ulr = request.url_for("admin_login_perform")
        if (e.msg):
            form.flash_message(tr.t(e.msg, request.state.locale), "danger")
        form.flash_form_values(form.to_dict())
        response = RedirectResponse(redirect_ulr, 303)
    return response


@router.get("/logout")
async def admin_logout(request: Request):
    redirect_ulr = request.url_for("admin_login")
    response = RedirectResponse(redirect_ulr, 303)
    response.delete_cookie("token")
    return response
