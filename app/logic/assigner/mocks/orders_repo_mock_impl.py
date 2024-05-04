import json
from typing import List

from app.core.repositories.models.orders_repo import OrdersRepo, OrderForAssign


class OrdersRepoMockImpl(OrdersRepo):

    async def get_fast_orders_without_driver(self) -> List[OrderForAssign]:
        with open('app/logic/assigner/fixtures/fast_orders.json') as f:
            slow_orders = json.loads(f.read())
        return [OrderForAssign(**order) for order in slow_orders]

    async def get_slow_orders_without_driver(self) -> List[OrderForAssign]:
        with open('app/logic/assigner/fixtures/slow_orders.json') as f:
            slow_orders = json.loads(f.read())
        return [OrderForAssign(**order) for order in slow_orders]

    async def get_fast_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        with open('app/logic/assigner/fixtures/fast_orders.json') as f:
            slow_orders = json.loads(f.read())
        return [OrderForAssign(**order) for order in slow_orders]

    async def get_slow_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        with open('app/logic/assigner/fixtures/slow_orders.json') as f:
            slow_orders = json.loads(f.read())
        return [OrderForAssign(**order) for order in slow_orders]
