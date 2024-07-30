import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .configuration.settings import settings

app_folder = os.path.dirname(__file__)


# API -> http://localhost/...

app = FastAPI(title=settings.app_name, version=settings.app_version)


@app.get("/health")
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
