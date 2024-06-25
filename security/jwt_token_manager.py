import abc
import jwt
from datetime import datetime, timedelta

ALGORITHM = "HS256"


class TokenExpiredError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


class JWTTokenManager(abc.ABC):
    @abc.abstractmethod
    def generate_auth_tokens(self, key: str):
        pass

    @abc.abstractmethod
    def verify_life_token(self, token: str):
        pass


class JWTTokenManagerImpl(JWTTokenManager):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def generate_auth_tokens(self, key: str):
        # Generar access token
        access_token_expires = timedelta(minutes=90)
        access_token_payload = {
            'uii': key,
            'exp': datetime.utcnow() + access_token_expires,
            'iat': datetime.utcnow()
        }
        access_token = jwt.encode(access_token_payload, self.secret_key, algorithm=ALGORITHM)

        # Generar refresh token
        refresh_token_expires = timedelta(days=2)
        refresh_token_payload = {
            'ui': key,
            'exp': datetime.utcnow() + refresh_token_expires,
            'iat': datetime.utcnow(),
        }
        refresh_token = jwt.encode(refresh_token_payload, self.secret_key, algorithm=ALGORITHM)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }

    def verify_life_token(self, token: str):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise TokenExpiredError("expired_token")
        except jwt.InvalidTokenError:
            raise InvalidTokenError("invalid_token")
