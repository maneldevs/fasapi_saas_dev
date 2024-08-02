from fastapi import APIRouter


router = APIRouter(prefix="/api/core/groups", tags=["Core - Groups"])


@router.get("/test")
async def test():
    return "inside groups"
