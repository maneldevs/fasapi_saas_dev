from fastapi import APIRouter

from .index_web import router as index_web_router
from .auth_web import router as auth_web_router
from .group_web import router as group_web_router
from .role_web import router as role_web_router
from .user_web import router as user_web_router

router = APIRouter()
router.include_router(index_web_router)
router.include_router(auth_web_router)
router.include_router(group_web_router)
router.include_router(role_web_router)
router.include_router(user_web_router)
