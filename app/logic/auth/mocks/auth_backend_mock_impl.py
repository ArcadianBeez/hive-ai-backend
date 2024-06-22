from app.core.gateway.auth_backend_impl import AuthBackendGateway


class AuthBackendMockImpl(AuthBackendGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def login_whatsapp(self, phone_number: str, code: str):
        return {"success": True, "data": {"api_token": "mocked_token"}, "message": "este usuario ya existe"}

    async def phone_verification_whatsapp(self, phone: str):
        return {"success": True,
                "data": True,
                "message": "queued"}
