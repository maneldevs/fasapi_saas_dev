import os
from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic_core import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
import src.app.configuration.exception_handler as handler
import src.app.configuration.exception_handler_admin as handler_admin
from src.app.modules.core.domain.dependencies import get_locale
from src.app.modules.core.utils.exceptions import BaseError
from src.app.modules.core.api import router as core_router
from src.app.modules.core.utils.middleware import AddUsernameMiddleware
from src.app.modules.core.web import router as core_web_router

from .configuration.settings import settings
from .configuration.lang import tr

app_folder = os.path.dirname(__file__)

# API -> http://localhost/api/...

app = FastAPI(title=settings.app_name, version=settings.app_version, dependencies=[Depends(get_locale)])
app.include_router(core_router)
app.add_exception_handler(BaseError, handler.base_handler)
app.add_exception_handler(RequestValidationError, handler.validation_handler)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "UP"}


# ADMIN WEB ->   # http://localhost/admin/...

admin = FastAPI(dependencies=[Depends(get_locale)])

app.mount("/static", StaticFiles(directory=app_folder + "/resources/static"), name="static")
app.mount("/admin", admin)
admin.include_router(core_web_router)
templates = Jinja2Templates(directory=app_folder + "/resources/templates")
templates.env.globals['_t'] = tr.t
admin.add_exception_handler(BaseError, handler_admin.base_handler)
# admin.add_exception_handler(ValidationError, handler_admin.validation_handler)
add_username_middleware = AddUsernameMiddleware()
admin.add_middleware(BaseHTTPMiddleware, dispatch=add_username_middleware)


@admin.get("/health", response_class=HTMLResponse)
async def admin_health(request: Request):
    return templates.TemplateResponse(request=request, name="health.html", context={})
