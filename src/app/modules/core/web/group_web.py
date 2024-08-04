from fastapi import APIRouter, Request
from src.app import main

router = APIRouter(prefix="/core/groups")


@router.get("/form")
async def form(request: Request):
    return main.templates.TemplateResponse(request=request, name="core/group_form.html", context={})
