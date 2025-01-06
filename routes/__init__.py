from fastapi import APIRouter
from .call_routes import router as call_router
from .user_routes import router as user_router

router = APIRouter()
router.include_router(call_router)
router.include_router(user_router)
