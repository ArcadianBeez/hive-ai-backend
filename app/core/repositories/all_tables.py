import datetime
from typing import List
import pymysql
from pymysql.cursors import DictCursor

from app.core.repositories.models.all_tables_repo import HiveQueriesRepo, ResponseHiveData

class HiveQueriesRepoImpl(HiveQueriesRepo):
    def __init__(self, db_config: dict):
        self.db_config = db_config

    def get_connection(self):
        connection = pymysql.connect(**self.db_config)
        with connection.cursor() as cursor:
            cursor.execute("SET time_zone = 'America/Guayaquil'")
        return connection

    async def fetch_by_query(self, query: str) -> List[ResponseHiveData]:
        connection = self.get_connection()
        cursor = connection.cursor(DictCursor)
        cursor.execute(query)
        responses = cursor.fetchall()
        cursor.close()
        connection.close()
        return [ResponseHiveData(**response) for response in responses]
