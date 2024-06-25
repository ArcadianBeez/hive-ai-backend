import abc

import inject

from security.jwt_token_manager import JWTTokenManager


class RefreshTokenUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, token: str):
        pass


class RefreshTokenUCImpl(RefreshTokenUC):
    jwt_token_manager: JWTTokenManager = inject.attr(JWTTokenManager)

    async def execute(self, token: str):
        try:
            payload = self.jwt_token_manager.verify_life_token(token)
            return self.jwt_token_manager.generate_auth_tokens(payload.get("uii"))
        except Exception as e:
            raise e
