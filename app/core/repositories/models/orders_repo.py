import abc
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field


class OrderForAssign(BaseModel):
    id: Optional[int] = Field(None, alias='id')
    user_id: Optional[int] = Field(None, alias='user_id')
    order_status_id: Optional[int] = Field(None, alias='order_status_id')
    created_at: Optional[datetime] = Field(None, alias='created_at')
    updated_at: Optional[datetime] = Field(None, alias='updated_at')
    preparation_time: Optional[int] = Field(None, alias='preparation_time')
    driver_id: Optional[int] = Field(None, alias='driver_id')
    order_address_id: Optional[int] = Field(None, alias='order_address_id')
    type: Optional[str] = Field(None, alias='type')
    received: Optional[int] = Field(None, alias='received')
    latitude_store: Optional[str] = Field(None, alias='latitude')
    longitude_store: Optional[str] = Field(None, alias='longitude')
    latitude_client: Optional[str] = Field(None, alias='latitude')
    longitude_client: Optional[str] = Field(None, alias='longitude')

    class Config:
        allow_population_by_field_name = True
        orm_mode = True


class OrdersRepo(abc.ABC):
    @abc.abstractmethod
    async def get_fast_orders_without_driver(self) -> List[OrderForAssign]:
        pass

    @abc.abstractmethod
    async def get_slow_orders_without_driver(self) -> List[OrderForAssign]:
        pass

    @abc.abstractmethod
    async def get_fast_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        pass

    @abc.abstractmethod
    async def get_slow_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        pass

    @abc.abstractmethod
    async def get_preparing_orders_without_driver_by_city(self, city_id) -> List[OrderForAssign]:
        pass
