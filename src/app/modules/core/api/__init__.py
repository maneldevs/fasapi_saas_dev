from fastapi import APIRouter

from .group import router as group_router

router = APIRouter()
router.include_router(group_router)
