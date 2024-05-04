import abc

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class DriverProfile(BaseModel):
    id: int = Field(None, alias='id')
    is_active: Optional[int] = Field(None, alias='is_active')
    status: int = Field(None, alias='status')
    device_token: Optional[str] = Field(None, alias='device_token')
    user_id: Optional[int] = Field(None, alias='user_id')
    created_at: Optional[datetime] = Field(None, alias='created_at')
    updated_at: Optional[datetime] = Field(None, alias='updated_at')
    max_orders: Optional[int] = Field(None, alias='max_orders')
    current_number_orders: Optional[int] = Field(None, alias='current_number_orders')
    latitude: Optional[str] = Field(None, alias='latitude')
    longitude: Optional[str] = Field(None, alias='longitude')
    is_working: Optional[int] = Field(None, alias='is_working')
    orders_count: Optional[int] = Field(None, alias='orders_count')
    completed_orders: Optional[int] = Field(None, alias='completed_orders')
    active_comision: Optional[float] = Field(None, alias='active_comision')
    reserve_complete: int = Field(None, alias='reserve_complete')
    rate_active_carriers: int = Field(None, alias='rate_active_carriers')
    backpack_code: Optional[str] = Field(None, alias='backpack_code')
    class_id: Optional[int] = Field(None, alias='class_id')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DriversProfileRepo(abc.ABC):
    @abc.abstractmethod
    async def get_available_drivers_profile(self) -> List[DriverProfile]:
        pass

    async def get_busy_drivers_profile(self) -> List[DriverProfile]:
        pass

    @abc.abstractmethod
    async def get_available_drivers_profile_by_city(self, city_id) -> List[DriverProfile]:
        pass

    async def get_busy_drivers_profile_by_city(self, city_id) -> List[DriverProfile]:
        pass
