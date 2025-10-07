from fastapi import APIRouter
from .webapp import router as webapp_router

# Combine the routers into one
router = APIRouter()

router.include_router(webapp_router, prefix="/api", tags=["Generate Answers"])
