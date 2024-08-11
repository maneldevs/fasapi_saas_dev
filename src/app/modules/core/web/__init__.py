from fastapi import APIRouter

from .group_web import router as group_web_router
from .role_web import router as role_web_router

router = APIRouter()
router.include_router(group_web_router)
router.include_router(role_web_router)
