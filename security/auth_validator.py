from decouple import config
from fastapi import Security, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, APIKeyHeader, HTTPAuthorizationCredentials
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_406_NOT_ACCEPTABLE, HTTP_404_NOT_FOUND

from security.jwt_token_manager import TokenExpiredError, InvalidTokenError, JWTTokenManagerImpl

jwt_scheme = HTTPBearer()
api_key_scheme = APIKeyHeader(name="API-KEY", auto_error=False)


def verify_auth(
        request: Request):
    token_service = JWTTokenManagerImpl(config("HIVE_BACKEND_API_KEY"))
    api_key = request.headers.get("api-key")
    auth_header = request.headers.get("Authorization")
    bearer = None
    if auth_header:
        bearer = HTTPAuthorizationCredentials(scheme="Bearer", credentials=auth_header.split(" ")[1])

    if api_key:
        # Verificar API key
        if api_key == config("THIS_NODE_API_KEY"):
            return True
        else:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="invalid_api_key")
    elif bearer:
        # Verificar JWT
        try:

            # Asumiendo que tienes un token_service para verificar JWTs
            token_service.verify_life_token(bearer.credentials)
            return True
        except TokenExpiredError:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="expired_token")
        except InvalidTokenError:
            raise HTTPException(status_code=HTTP_406_NOT_ACCEPTABLE, detail="invalid_token")
    else:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND)
