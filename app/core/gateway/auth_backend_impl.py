import abc
import json

import httpx


class AuthBackendGateway(abc.ABC):
    @abc.abstractmethod
    def login_whatsapp(self, phone: str, code: str) -> dict:
        pass

    @abc.abstractmethod
    def phone_verification_whatsapp(self, phone: str):
        pass


class AuthBackendGatewayImpl(AuthBackendGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def phone_verification_whatsapp(self, phone: str):
        url = f"{self.base_url}/api/phone_verification"
        payload = {
            "number": phone,
            "type": "whatsapp"
        }
        client = httpx.AsyncClient(verify=False)
        try:
            response = await client.post(
                url,
                timeout=60,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except httpx.RequestError as e:
            print(f"1Error fetching data: {e}")
            return []
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return json.loads(e.response.content.decode())
        finally:
            await client.aclose()  # Ensure the client is closed regardless of the earlier outcomes

    async def login_whatsapp(self, phone: str, code: str) -> dict:
        url = f"{self.base_url}/api/login_whatsapp"
        payload = {
            "code": code,
            "number": phone
        }
        client = httpx.AsyncClient(verify=False)
        try:
            response = await client.post(
                url,
                timeout=60,
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except httpx.RequestError as e:
            print(f"1Error fetching data: {e}")
            return []
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return json.loads(e.response.content.decode())
        finally:
            await client.aclose()  # Ensure the client is closed regardless of the earlier outcomes
