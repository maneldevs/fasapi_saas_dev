from fastapi import Request
from fastapi.responses import RedirectResponse
from src.app.configuration.exceptions import BaseError


def base_handler(request: Request, exc: BaseError):
    redirect_ulr = request.url_for("admin_login").include_query_params(msg=exc.msg)
    return RedirectResponse(redirect_ulr, 303)
