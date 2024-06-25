import inject
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE

from app.logic.auth.login_whatsapp import LoginWhatsAppUC
from app.logic.auth.phone_verification_whatsapp import PhoneVerificationWhatsAppUC
from app.logic.auth.refresh_token import RefreshTokenUC
from security.jwt_token_manager import TokenExpiredError, InvalidTokenError


class PhoneVerificationRequest(BaseModel):
    phone: str


class LoginRequest(BaseModel):
    phone: str
    code: str


class RefreshTokenRequest(BaseModel):
    token: str


auth_router = APIRouter()


@auth_router.post("/phone_verification")
async def phone_verification_whatsapp(body: PhoneVerificationRequest):
    uc = inject.instance(PhoneVerificationWhatsAppUC)
    response = await uc.execute(body.phone)
    return response


@auth_router.post("/login", )
async def login_whatsapp(body: LoginRequest):
    uc = inject.instance(LoginWhatsAppUC)
    response = await uc.execute(body.phone, body.code)
    return response


@auth_router.post("/refresh")
async def refresh_token(body: RefreshTokenRequest):
    uc = inject.instance(RefreshTokenUC)
    try:
        response = await uc.execute(body.token)
        return {"success": True, **response}
    except TokenExpiredError:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="expired_token")
    except InvalidTokenError:
        raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE, detail="invalid_token")
