import pytest
from decouple import config

from app.core.gateway.auth_backend_impl import AuthBackendGatewayImpl


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_get_response_verify_code_whatsapp():
    auth_gateway = AuthBackendGatewayImpl(base_url=config("HIVE_BACKEND_URL"))
    phone = "+593989778128"
    response = await auth_gateway.phone_verification_whatsapp(phone)
    assert response is not None  # Or other appropriate assertions


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_get_response_login_whatsapp():
    auth_gateway = AuthBackendGatewayImpl(base_url=config("HIVE_BACKEND_URL"))
    phone = "+593989778128"
    code = "403174"
    response = await auth_gateway.login_whatsapp(phone, code)
    assert response is not None  # Or other appropriate assertions
