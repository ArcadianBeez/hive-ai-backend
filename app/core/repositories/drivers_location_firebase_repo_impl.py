import json
from typing import List

from firebase_admin.db import Reference

from app.core.repositories.models.drivers_location_repo import DriversLocationRepo, DriverInfo, Order


class DriversLocationRepoFirebaseImpl(DriversLocationRepo):
    def __init__(self, ref: Reference):
        self.ref_database = ref

    def get_drivers_location(self) -> List[DriverInfo]:
        drivers = self.ref_database.get()
        drivers_list: List[DriverInfo] = []
        for clave, valor in drivers.items():
            try:

                orders_str = valor["orders"]
                del valor["orders"]
                orders_json = json.loads(orders_str)

                valor["orders"] = [Order(**order) for order in orders_json]
                driver_info = DriverInfo(**valor)

                driver_info.user_id = clave
                drivers_list.append(driver_info)
            except Exception as e:
                print(f"Error al parsear el driver {clave}: {e}")

        return drivers_list

    async def get_driver_location_by_id(self, driver_id: str) -> DriverInfo:
        driver = self.ref_database.child(driver_id).get()
        try:
            orders_str = driver["orders"]
            del driver["orders"]
            orders_json = json.loads(orders_str)

            driver["orders"] = [Order(**order) for order in orders_json]
            driver_info = DriverInfo(**driver)

            driver_info.user_id = driver_id
            return driver_info
        except Exception as e:
            print(f"Error al parsear el driver {driver_id}: {e}")
            return None
