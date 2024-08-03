import os
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import src.app.configuration.exception_handler as handler
from src.app.configuration.exceptions import BaseError
from src.app.modules.core.api import router as core_router

from .configuration.settings import settings

app_folder = os.path.dirname(__file__)


# API -> http://localhost/api/...

app = FastAPI(title=settings.app_name, version=settings.app_version)
app.include_router(core_router)
app.add_exception_handler(BaseError, handler.base_handler)
app.add_exception_handler(RequestValidationError, handler.validation_handler)


@app.get("/api/health")
async def health() -> dict:
    return {"status": "UP"}


# ADMIN WEB ->   # http://localhost/admin/...

admin = FastAPI()

app.mount("/static", StaticFiles(directory=app_folder + "/resources/static"), name="static")
app.mount("/admin", admin)

templates = Jinja2Templates(directory=app_folder + "/resources/templates")


@admin.get("/health", response_class=HTMLResponse)
async def admin_health(request: Request):
    return templates.TemplateResponse(request=request, name="health.html", context={})
