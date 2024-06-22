import inject
from fastapi import APIRouter, Query
from pydantic import BaseModel

from app.logic.auth.login_whatsapp import LoginWhatsAppUC
from app.logic.auth.phone_verification_whatsapp import PhoneVerificationWhatsAppUC


class LoginRequest(BaseModel):
    phone: str
    code: str


auth_router = APIRouter()


@auth_router.get("/phone_verification")
async def phone_verification_whatsapp(phone: str = Query(
    ...,
    title="Phone number",
    description="Phone number to verify",
    min_length=13,
    max_length=13
)):
    uc = inject.instance(PhoneVerificationWhatsAppUC)
    response = await uc.execute(phone)
    return response


@auth_router.post("/login",)
async def login_whatsapp(body: LoginRequest):
    uc = inject.instance(LoginWhatsAppUC)
    response = await uc.execute(body.phone, body.code)
    return response
