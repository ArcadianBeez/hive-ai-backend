import abc

import inject

from app.core.gateway.auth_backend_impl import AuthBackendGateway
from security.jwt_token_manager import JWTTokenManager


class LoginWhatsAppUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, phone_number: str, code: str):
        pass


class LoginWhatsAppUCImpl(LoginWhatsAppUC):
    auth_gateway: AuthBackendGateway = inject.attr(AuthBackendGateway)
    jwt_token_manager: JWTTokenManager = inject.attr(JWTTokenManager)

    async def execute(self, phone_number: str, code: str):
        try:
            response = await self.auth_gateway.login_whatsapp(phone_number, code)
            if response.get("success"):
                tokens = self.jwt_token_manager.generate_auth_tokens(response.get("api_token"))
                return {"success": True, **tokens}
            else:
                return {"success": False, "message": "Invalid phone number or code"}
        except Exception as e:
            return {"status": False, "message": str(e)}
