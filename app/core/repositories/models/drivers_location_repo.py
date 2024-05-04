import abc
from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional


class Order(BaseModel):
    id: Optional[str] = Field(None, alias="orderId")
    store_lat: Optional[float] = Field(None, alias="storeLatitude")
    store_long: Optional[float] = Field(None, alias="storeLongitude")
    client_lat: Optional[float] = Field(None, alias="clientLatitude")
    client_long: Optional[float] = Field(None, alias="clientLongitude")
    status: Optional[str] = Field(None, alias="orderStatus")
    order_status_id: Optional[str] = Field(None, alias="statusId")

    class Config:
        allow_population_by_field_name = True


class DriverInfo(BaseModel):
    user_id: Optional[int] = Field(None, alias="userId")
    city_id: Optional[int] = Field(None, alias="cityId")
    date: Optional[str] = Field(None, alias="dateInfo")
    icon: Optional[HttpUrl] = Field(None, alias="iconUrl")
    is_working: Optional[int] = Field(None, alias="workingStatus")
    latitude: Optional[float] = Field(None, alias="lat")
    longitude: Optional[float] = Field(None, alias="long")
    orders: Optional[List[Order]] = Field(None, alias="currentOrders")
    userName: Optional[str] = Field(None, alias="username")

    class Config:
        allow_population_by_field_name = True


class DriversLocationRepo(abc.ABC):
    @abc.abstractmethod
    async def get_drivers_location(self) -> List[DriverInfo]:
        pass

    @abc.abstractmethod
    async def get_driver_location_by_id(self, driver_id: str) -> DriverInfo:
        pass
