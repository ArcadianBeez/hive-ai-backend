from fastapi import APIRouter

from app.output.router import order_assigner_router

app_router = APIRouter()
app_router.include_router(order_assigner_router, prefix="/queries", tags=["Queries"])
