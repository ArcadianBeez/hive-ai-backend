import inject
import pytest
from decouple import config

from app.core.gateway.auth_backend_impl import AuthBackendGateway
from app.logic.auth.login_whatsapp import LoginWhatsAppUCImpl
from app.logic.auth.mocks.auth_backend_mock_impl import AuthBackendMockImpl


def my_config(binder):
    binder.bind(AuthBackendGateway, AuthBackendMockImpl(base_url=config("HIVE_BACKEND_URL")))


@pytest.fixture
def inject_live_config():
    inject.clear_and_configure(my_config)


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_login_with_whatsapp(inject_live_config):
    uc = LoginWhatsAppUCImpl()
    phone = "+593989778128"
    code = "943250"
    response = await uc.execute(phone, code)
    assert response is not None
