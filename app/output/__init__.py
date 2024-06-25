from fastapi import APIRouter, Depends

from app.output.router import order_assigner_router
from app.output.auth_router import auth_router
from security.auth_validator import verify_auth

app_router = APIRouter()
app_router.include_router(auth_router, prefix="/auth", tags=["Auth"])
app_router.include_router(order_assigner_router, prefix="/queries", tags=["Queries"],
                          dependencies=[Depends(verify_auth)])
