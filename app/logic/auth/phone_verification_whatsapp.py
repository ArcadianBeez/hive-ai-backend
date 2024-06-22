import abc

import inject

from app.core.gateway.auth_backend_impl import AuthBackendGateway


class PhoneVerificationWhatsAppUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, phone: str):
        pass


class PhoneVerificationWhatsAppUCImpl(PhoneVerificationWhatsAppUC):
    auth_gateway: AuthBackendGateway = inject.attr(AuthBackendGateway)

    async def execute(self, phone: str):
        response = await self.auth_gateway.phone_verification_whatsapp(phone)
        return response
