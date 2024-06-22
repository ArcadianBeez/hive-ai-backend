import abc

import inject

from app.core.gateway.auth_backend_impl import AuthBackendGateway
from security.jwt_token_manager import generate_auth_tokens


class LoginWhatsAppUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, phone_number: str, code: str):
        pass


class LoginWhatsAppUCImpl(LoginWhatsAppUC):
    auth_gateway: AuthBackendGateway = inject.attr(AuthBackendGateway)

    async def execute(self, phone_number: str, code: str):
        try:
            response = await self.auth_gateway.login_whatsapp(phone_number, code)
            if response.get("status") == "success":
                tokens = generate_auth_tokens(response.get("user_id"))
                response["tokens"] = tokens
            return response
        except Exception as e:
            return {"status": "error", "message": str(e)}

