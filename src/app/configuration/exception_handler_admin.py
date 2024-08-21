from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import RedirectResponse
from src.app.modules.core.utils.exceptions import BaseError
from src.app import main


def base_handler(request: Request, exc: BaseError):
    redirect_ulr = request.url_for("admin_login").include_query_params(msg=exc.msg)
    return RedirectResponse(redirect_ulr, 303)


# TODO mmr intentar sacar aquí un handler para validación que haga parte de lo que hace ahora forms
# async def validation_handler(request: Request, exc: RequestValidationError):
#     print(exc.errors())
#     return RedirectResponse(request.url, 303)