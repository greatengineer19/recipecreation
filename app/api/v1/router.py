from fastapi import APIRouter

from app.api.v1.endpoints.items import router as items_router
from app.api.v1.endpoints.recipes import router as recipes_router

api_router = APIRouter()
api_router.include_router(items_router)
api_router.include_router(recipes_router)
