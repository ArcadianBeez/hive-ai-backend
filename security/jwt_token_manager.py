import abc
import jwt
from datetime import datetime, timedelta
from decouple import config


class TokenExpiredError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


SECRET_KEY = config("HIVE_BACKEND_API_KEY")
ALGORITHM = "HS256"


def generate_auth_tokens(key: str):
    # Generar access token
    access_token_expires = timedelta(minutes=90)
    access_token_payload = {
        'uii': key,
        'exp': datetime.utcnow() + access_token_expires,
        'iat': datetime.utcnow()
    }
    access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    # Generar refresh token
    refresh_token_expires = timedelta(days=2)
    refresh_token_payload = {
        'ui': key,
        'exp': datetime.utcnow() + refresh_token_expires,
        'iat': datetime.utcnow(),
    }
    refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }


def verify_life_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("El token ha expirado")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("El token es inválido")
