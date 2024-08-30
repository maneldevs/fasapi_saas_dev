from fastapi import APIRouter

from .auth_api import router as auth_router
from .group_api import router as group_router
from .role_api import router as role_router
from .user_api import router as user_router
from .module_api import router as module_router
from .resources_api import router as resources_router
from .permission_api import router as permission_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(group_router)
router.include_router(role_router)
router.include_router(user_router)
router.include_router(module_router)
router.include_router(resources_router)
router.include_router(permission_router)
