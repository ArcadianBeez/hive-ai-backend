import abc
from typing import List
import httpx


class DistanceMatrixGateway(abc.ABC):
    @abc.abstractmethod
    def get_distance_matrix(self, origin, destination):
        pass


class DistanceMatrixOsmImpl(DistanceMatrixGateway):
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_distance_matrix(self, origins: List[str], destinations: List[str]) -> List[List[float]]:
        # Join the origins and destinations into a single string with semicolons
        origins_str = ";".join(origins)
        destinations_str = ";".join(destinations)

        # Construct the complete URL
        url = f"{self.base_url}/table/v1/driving/{destinations_str};{origins_str}?destinations=0&annotations=distance"

        client = httpx.AsyncClient(verify=False)  # Create an instance of AsyncClient here

        try:
            response = await client.get(url, timeout=30)  # SSL verification is disabled
            response.raise_for_status()  # Raises an HTTPError for bad responses
            json_data = response.json()

            if json_data.get('code') == "Ok":
                # Remove the first distance from the main array
                distances = [element[0] for element in json_data['distances'][1:]]
                return distances
        except httpx.RequestError as e:
            print(f"Error fetching data: {e}")
            return []
        finally:
            await client.aclose()  # Ensure the client is closed regardless of the earlier outcomes
