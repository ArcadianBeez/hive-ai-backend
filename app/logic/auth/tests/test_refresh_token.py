import inject
import pytest
from decouple import config

from app.core.gateway.auth_backend_impl import AuthBackendGateway
from app.logic.auth.login_whatsapp import LoginWhatsAppUCImpl
from app.logic.auth.mocks.auth_backend_mock_impl import AuthBackendMockImpl
from app.logic.auth.refresh_token import RefreshTokenUCImpl
from security.jwt_token_manager import JWTTokenManagerImpl, JWTTokenManager


def my_config(binder):
    binder.bind(JWTTokenManager, JWTTokenManagerImpl(secret_key=config("HIVE_BACKEND_API_KEY")))


@pytest.fixture
def inject_live_config():
    inject.clear_and_configure(my_config)


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_refresh_token(inject_live_config):
    uc = RefreshTokenUCImpl()
    expired_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aSI6bnVsbCwiZXhwIjoxNzE5NTMwMTM1LCJpYXQiOjE3MTkzNTczMzV9.fyXwgSAs7_mhuH5FqSSFiipYOrIArg7cd6UNTOx1I3o"
    response = await uc.execute(expired_token)
    print(response)
    assert response is not None
