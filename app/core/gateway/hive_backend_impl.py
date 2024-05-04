import abc

import httpx


class HiveBackendGateway(abc.ABC):
    @abc.abstractmethod
    def assign_free_order(self, driver_id: str, order_id: str):
        pass


class HiveBackendGatewayImpl(HiveBackendGateway):
    def __init__(self, base_url: str, api_token: str):
        self.base_url = base_url
        self.api_token = api_token

    async def assign_free_order(self, driver_id: str, order_id: str):
        url = f"{self.base_url}/api/assignOrderToDriver?api_token={self.api_token}"
        payload = {
            "id": order_id,
            "driver_id": driver_id
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
            print(f"Error fetching data: {e}")
            return []
        finally:
            await client.aclose()  # Ensure the client is closed regardless of the earlier outcomes
