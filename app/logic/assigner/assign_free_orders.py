import abc
from typing import List

import inject
from loguru import logger
from pydantic import BaseModel
import asyncio
from app.core.gateway.distance_matrix_osm_impl import DistanceMatrixGateway
from app.core.gateway.hive_backend_impl import HiveBackendGateway
from app.core.repositories.models.drivers_location_repo import DriversLocationRepo
from app.core.repositories.models.drivers_profile_repo import DriversProfileRepo
from app.core.repositories.models.orders_repo import OrdersRepo


class AssignFreeOrdersUC(abc.ABC):
    @abc.abstractmethod
    async def execute(self, city_id: str, fast_order_radius: int, slow_order_radius: int) -> dict:
        pass


class DistanceDriver(BaseModel):
    driver_id: str
    latitude: float
    longitude: float


class DistanceDriverOrder(BaseModel):
    driver_id: str
    order_id: str
    distance: float


class AssignFreeOrdersUCImpl(AssignFreeOrdersUC):
    orders_repo: OrdersRepo = inject.attr(OrdersRepo)
    drivers_location_repo: DriversLocationRepo = inject.attr(DriversLocationRepo)
    drivers_profile_repo: DriversProfileRepo = inject.attr(DriversProfileRepo)
    distance_matrix_gateway: DistanceMatrixGateway = inject.attr(DistanceMatrixGateway)
    hive_backend_gateway: HiveBackendGateway = inject.attr(HiveBackendGateway)

    async def execute(self, city_id: str, fast_order_radius: int, slow_order_radius: int) -> dict:

        instant_orders, slow_orders, preparing_orders = await self.fetch_orders(city_id)
        active_drivers, busy_drivers = await self.fetch_drivers(city_id)


        locations_drivers_available = await self.get_driver_locations(active_drivers)
        locations_drivers_busy = await self.get_driver_locations(busy_drivers)

        orders_drivers_instant_distance = await self.calculate_distances(instant_orders, locations_drivers_available)
        orders_drivers_preparing_distance = await self.calculate_distances(preparing_orders, locations_drivers_available)
        orders_drivers_slow_distance = await self.calculate_distances(slow_orders, locations_drivers_busy)


        min_distances_instant_orders = self.select_min_distances(orders_drivers_instant_distance)
        min_distances_preparing_orders = self.select_min_distances(orders_drivers_preparing_distance)
        min_distances_slow = self.select_min_distances(orders_drivers_slow_distance)

        tasks = []
        selected_drivers = set()
        for entry in min_distances_instant_orders:

            if entry.distance < fast_order_radius:
                selected_drivers.add(entry.driver_id)
                tasks.append(self.hive_backend_gateway.assign_free_order(entry.driver_id, entry.order_id))
                logger.info(f"Assigning order {entry.order_id} to driver {entry.driver_id} in {entry.distance} meters")
            else:
                logger.info(
                    f"Order {entry.order_id} is too far away from driver {entry.driver_id} ({entry.distance} meters)")

        for entry in min_distances_preparing_orders:
            if entry.driver_id not in selected_drivers and entry.distance < fast_order_radius:
                tasks.append(self.hive_backend_gateway.assign_free_order(entry.driver_id, entry.order_id))
                logger.info(f"Assigning order {entry.order_id} to driver {entry.driver_id} in {entry.distance} meters")
            else:
                logger.info(
                    f"Order {entry.order_id} is too far away from driver {entry.driver_id} ({entry.distance} meters)")

        for entry in min_distances_slow:
            if entry.distance < slow_order_radius:
                logger.info(f"Assigning order {entry.order_id} to driver {entry.driver_id} in {entry.distance} meters")
                tasks.append(self.hive_backend_gateway.assign_free_order(entry.driver_id, entry.order_id))
            else:
                logger.info(
                    f"Order {entry.order_id} is too far away from driver {entry.driver_id} ({entry.distance} meters)")

        await asyncio.gather(*tasks)
        return {
            "fast_orders": [entry.order_id for entry in min_distances_instant_orders],
            "slow_orders": [entry.order_id for entry in min_distances_slow]
        }

    async def fetch_orders(self, city_id):
        # Fetch both sets of orders concurrently
        tasks = []
        tasks.append(self.orders_repo.get_fast_orders_without_driver_by_city(city_id))
        tasks.append(self.orders_repo.get_slow_orders_without_driver_by_city(city_id))
        tasks.append(self.orders_repo.get_preparing_orders_without_driver_by_city(city_id))

        instant_orders, slow_orders, preparing_orders = await asyncio.gather(*tasks)
        return instant_orders, slow_orders, preparing_orders

    async def fetch_drivers(self, city_id):
        tasks = []
        tasks.append(self.drivers_profile_repo.get_available_drivers_profile_by_city(city_id))
        tasks.append(self.drivers_profile_repo.get_busy_drivers_profile_by_city(city_id))
        active_drivers, busy_drivers = await asyncio.gather(*tasks)
        return active_drivers, busy_drivers

    async def fetch_active_drivers(self):
        return await self.drivers_profile_repo.get_available_drivers_profile()

    async def fetch_busy_drivers(self):
        return await self.drivers_profile_repo.get_busy_drivers_profile()

    async def get_driver_locations(self, active_drivers):
        locations = []
        for driver in active_drivers:
            location = await self.drivers_location_repo.get_driver_location_by_id(str(driver.user_id))
            if location is not None:
                locations.append(
                    DistanceDriver(driver_id=driver.user_id, latitude=location.latitude, longitude=location.longitude))
        return locations

    async def calculate_distances(self, orders, drivers):
        orders_drivers_distance = []
        for order in orders:
            driver_strs = [f"{driver.longitude},{driver.latitude}" for driver in drivers]
            if len(driver_strs) > 0:
                store_location = f"{order.longitude_store},{order.latitude_store}"
                distances = await self.distance_matrix_gateway.get_distance_matrix(driver_strs, [store_location])
                for distance, driver in zip(distances, drivers):
                    orders_drivers_distance.append(
                        DistanceDriverOrder(driver_id=driver.driver_id, order_id=order.id, distance=distance))
        return orders_drivers_distance

    def select_min_distances(self, entries: List[DistanceDriverOrder]):
        sorted_entries = sorted(entries, key=lambda x: x.distance)
        min_distance_by_order = {}
        selected_drivers = set()
        for entry in sorted_entries:
            if entry.driver_id not in selected_drivers and entry.order_id not in min_distance_by_order:
                min_distance_by_order[entry.order_id] = entry
                selected_drivers.add(entry.driver_id)
        return list(min_distance_by_order.values())
