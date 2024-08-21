from typing import Annotated
from fastapi import APIRouter, Depends, Request

from src.app import main
from src.app.modules.core.domain.dependencies import principal_god
from src.app.modules.core.domain.services.statistics_service import StatisticsService


router = APIRouter(prefix="/core", dependencies=[Depends(principal_god)])


@router.get("/")
async def admin_index(request: Request, service: Annotated[StatisticsService, Depends()], msg: str = None):
    context = service.counts().model_dump()
    if (msg):
        context |= {"msg": msg, "type": "success"}
    return main.templates.TemplateResponse(request=request, name="core/index.html", context=context)
