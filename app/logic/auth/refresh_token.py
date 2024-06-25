import abc

from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE

from security.jwt_token_manager import verify_life_token, generate_auth_tokens, InvalidTokenError, TokenExpiredError


class RefreshTokenUC(abc.ABC):
    @abc.abstractmethod
    def execute(self, token: str):
        pass


class RefreshTokenUCImpl(RefreshTokenUC):

    async def execute(self, token: str):
        try:
            payload = verify_life_token(token)
            return generate_auth_tokens(payload.get("uii"))
        except Exception as e:
            raise e
