import abc


class RefreshTokenUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, token: str) -> dict:
        pass


class RefreshTokenUCImpl(RefreshTokenUC):
    def __init__(self, jwt_manager):
        self.jwt_manager = jwt_manager

    async def execute(self, token: str) -> dict:
        try:
            payload = self.jwt_manager.verify_token(token)
            return self.jwt_manager.generate_tokens(payload.get("key"))
        except self.jwt_manager.TokenExpiredError:
            return {"error": "Token expirado"}
        except self.jwt_manager.InvalidTokenError:
            return {"error": "Token inválido"}
