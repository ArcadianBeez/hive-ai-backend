from typing import List

import pymysql
from pymysql.cursors import DictCursor

from app.core.repositories.models.drivers_profile_repo import DriversProfileRepo, DriverProfile


class DriversProfileMySQLRepoImpl(DriversProfileRepo):
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.table_name = "active_carriers"
        self.join1 = "users_cities"

    def get_connection(self):
        connection = pymysql.connect(**self.db_config)
        return connection

    async def get_available_drivers_profile(self) -> List[DriverProfile]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        cursor.execute(f"SELECT * FROM {self.table_name} WHERE is_active = 1 AND status =1 AND is_working = 1")
        drivers = cursor.fetchall()
        cursor.close()
        connection.close()
        return [DriverProfile(**driver) for driver in drivers]

    async def get_busy_drivers_profile(self) -> List[DriverProfile]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        cursor.execute(
            f"SELECT * FROM {self.table_name} WHERE is_active = 0 AND status =1 AND is_working = 1 AND current_number_orders =1")
        drivers = cursor.fetchall()
        cursor.close()
        connection.close()
        return [DriverProfile(**driver) for driver in drivers]

    async def get_available_drivers_profile_by_city(self, city_id) -> List[DriverProfile]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        cursor.execute(
            f"SELECT * "
            f"FROM {self.table_name} "
            f"JOIN {self.join1} dc ON {self.table_name}.user_id = dc.user_id "
            f"WHERE {self.table_name}.is_active = 1"
            f" AND dc.city_id = {city_id}"
            f" AND {self.table_name}.status = 1  "
            f" AND {self.table_name}.is_working = 1"
        )

        drivers = cursor.fetchall()
        cursor.close()
        connection.close()
        return [DriverProfile(**driver) for driver in drivers]

    async def get_busy_drivers_profile_by_city(self, city_id) -> List[DriverProfile]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        cursor.execute(
            f"SELECT * "
            f"FROM {self.table_name} "
            f"JOIN {self.join1} dc ON {self.table_name}.user_id = dc.user_id "
            f"WHERE {self.table_name}.is_active = 0"
            f" AND current_number_orders =1"
            f" AND dc.city_id = {city_id}"
            f" AND {self.table_name}.status = 1"
            f" AND {self.table_name}.is_working = 1"
        )

        drivers = cursor.fetchall()
        cursor.close()
        connection.close()
        return [DriverProfile(**driver) for driver in drivers]
