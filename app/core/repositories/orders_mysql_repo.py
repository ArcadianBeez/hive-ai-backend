import datetime
from typing import List
import pymysql
import pytz
from pymysql.cursors import DictCursor
from app.core.repositories.models.orders_repo import OrderForAssign, OrdersRepo


class OrderMySQLRepoImpl(OrdersRepo):
    def __init__(self, db_config: dict):
        self.db_config = db_config
        self.table_name = "orders"
        self.join1 = "restaurants"
        self.join2 = "order_address"
        self.join3 = "restaurants_city"

    def get_connection(self):
        connection = pymysql.connect(**self.db_config)
        return connection

    async def get_fast_orders_without_driver(self) -> List[OrderForAssign]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        date_now_str = self.get_current_date_ecuador()
        query = (
            f"SELECT "
            f"{self.table_name}.id, "
            f"user_id, "
            f"order_status_id, "
            f"{self.table_name}.created_at AS created_at, "
            f"{self.table_name}.updated_at AS updated_at, "
            f"driver_id, "
            f"order_address_id, "
            f"received, "
            f"preparation_time,"
            f"s.latitude AS latitude_store, "
            f"s.longitude AS longitude_store, "
            f"oa.latitude AS latitude_client, "
            f"oa.longitude AS longitude_client "
            f"FROM {self.table_name} "
            f"JOIN {self.join1} s ON {self.table_name}.restaurant_id = s.id "
            f"JOIN {self.join2} oa ON {self.table_name}.order_address_id = oa.id "
            f"WHERE order_status_id NOT IN (1, 6, 7, 8) "
            f"AND preparation_time <= 30 "
            f"AND {self.table_name}.created_at > '{date_now_str}'"
            f"AND {self.table_name}.driver_id IS NULL"
        )
        cursor.execute(query)

        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return [OrderForAssign(**order) for order in orders]

    async def get_slow_orders_without_driver(self) -> List[OrderForAssign]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        date_now_str = self.get_current_date_ecuador()
        cursor.execute(
            f"SELECT "
            f"{self.table_name}.id, "
            f"user_id, "
            f"order_status_id, "
            f"{self.table_name}.created_at as created_at, "
            f"{self.table_name}.updated_at as updated_at, "
            f"driver_id, "
            f"order_address_id, "
            f"received,"
            f"preparation_time,"
            f"s.latitude as latitude_store,"
            f"s.longitude as longitude_store, "
            f"oa.latitude as latitude_client, "
            f"oa.longitude as longitude_client  "
            f"FROM {self.table_name}"
            f" JOIN {self.join1} s ON {self.table_name}.restaurant_id = s.id"
            f" JOIN {self.join2} oa ON {self.table_name}.order_address_id = oa.id"
            f" WHERE order_status_id NOT in (1, 6, 7, 8)"
            f" AND preparation_time > 30"
            f" AND {self.table_name}.created_at > '{date_now_str}'"
            f" AND {self.table_name}.driver_id IS NULL"
        )

        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return [OrderForAssign(**order) for order in orders]

    async def get_fast_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        date_now_str = self.get_current_date_ecuador()
        query = (
            f"SELECT "
            f"{self.table_name}.id, "
            f"user_id, "
            f"order_status_id, "
            f"{self.table_name}.created_at AS created_at, "
            f"{self.table_name}.updated_at AS updated_at, "
            f"driver_id, "
            f"order_address_id, "
            f"received, "
            f"preparation_time,"
            f"s.latitude AS latitude_store, "
            f"s.longitude AS longitude_store, "
            f"oa.latitude AS latitude_client, "
            f"oa.longitude AS longitude_client, "
            f"sc.city_id AS order_city_id "
            f"FROM {self.table_name} "
            f"JOIN {self.join1} s ON {self.table_name}.restaurant_id = s.id "
            f"JOIN {self.join2} oa ON {self.table_name}.order_address_id = oa.id "
            f"JOIN {self.join3} sc ON s.id = sc.restaurants_id "
            f"WHERE order_status_id NOT IN (1, 6, 7, 8, 3) "
            f"AND sc.city_id = {city_id} "
            f"AND preparation_time <= 30 "
            f"AND {self.table_name}.created_at > '{date_now_str}'"
            f"AND {self.table_name}.driver_id IS NULL"
        )

        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return [OrderForAssign(**order) for order in orders]


    async def get_preparing_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        date_now_str = self.get_current_date_ecuador()
        query = (
            f"SELECT "
            f"{self.table_name}.id, "
            f"user_id, "
            f"order_status_id, "
            f"{self.table_name}.created_at AS created_at, "
            f"{self.table_name}.updated_at AS updated_at, "
            f"driver_id, "
            f"order_address_id, "
            f"received, "
            f"preparation_time,"
            f"s.latitude AS latitude_store, "
            f"s.longitude AS longitude_store, "
            f"oa.latitude AS latitude_client, "
            f"oa.longitude AS longitude_client, "
            f"sc.city_id AS order_city_id "
            f"FROM {self.table_name} "
            f"JOIN {self.join1} s ON {self.table_name}.restaurant_id = s.id "
            f"JOIN {self.join2} oa ON {self.table_name}.order_address_id = oa.id "
            f"JOIN {self.join3} sc ON s.id = sc.restaurants_id "
            f"WHERE order_status_id IN (3) "
            f"AND sc.city_id = {city_id} "
            f"AND preparation_time <= 30 "
            f"AND {self.table_name}.created_at > '{date_now_str}'"
            f"AND {self.table_name}.driver_id IS NULL"
        )

        cursor.execute(query)
        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return [OrderForAssign(**order) for order in orders]

    async def get_slow_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        date_now_str = self.get_current_date_ecuador()
        cursor.execute(
            f"SELECT "
            f"{self.table_name}.id, "
            f"user_id, "
            f"order_status_id, "
            f"{self.table_name}.created_at as created_at, "
            f"{self.table_name}.updated_at as updated_at, "
            f"driver_id, "
            f"order_address_id, "
            f"received,"
            f"preparation_time,"
            f"s.latitude as latitude_store,"
            f"s.longitude as longitude_store, "
            f"oa.latitude as latitude_client, "
            f"oa.longitude as longitude_client,  "
            f"sc.city_id AS order_city_id "
            f"FROM {self.table_name}"
            f" JOIN {self.join1} s ON {self.table_name}.restaurant_id = s.id"
            f" JOIN {self.join2} oa ON {self.table_name}.order_address_id = oa.id"
            f" JOIN {self.join3} sc ON s.id = sc.restaurants_id "
            f" WHERE order_status_id NOT in (1, 6, 7, 8)"
            f"AND sc.city_id = {city_id} "
            f" AND preparation_time > 30"
            f" AND {self.table_name}.created_at > '{date_now_str}'"
            f" AND {self.table_name}.driver_id IS NULL"
        )

        orders = cursor.fetchall()
        cursor.close()
        connection.close()
        return [OrderForAssign(**order) for order in orders]

    def get_current_date_ecuador(selg):
        # Define the time zone for Ecuador
        ecuador_timezone = pytz.timezone('America/Guayaquil')

        # Get the current UTC date and time
        date_utc = datetime.datetime.now(pytz.utc)

        # Convert the UTC date and time to Ecuador's time zone
        date_ecuador = date_utc.astimezone(ecuador_timezone)

        # Format the date as a string in the format YYYY-MM-DD
        date_str = date_ecuador.strftime("%Y-%m-%d")
        return date_str
