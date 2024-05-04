from typing import Optional

from decouple import config
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

api_key_scheme = APIKeyHeader(name="API-KEY", auto_error=False)


async def validate_apikey_request(
        api_key: str = Security(api_key_scheme),
) -> Optional[bool]:
    """Validate a request with given email and api key
    to any endpoint resource
    """
    # verify email & API key
    if api_key == config("THIS_NODE_API_KEY"):
        return True
    else:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
        )
