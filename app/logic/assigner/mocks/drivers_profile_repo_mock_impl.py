from typing import List

from app.core.repositories.models.drivers_profile_repo import DriverProfile, DriversProfileRepo


class DriversProfileRepoMockImpl(DriversProfileRepo):

    def __init__(self):
        self.profile_drivers = [
            {
                "id": 1,
                "is_active": 1,
                "status": 2,
                "device_token": "abc123xyz",
                "user_id": 627,
                "created_at": "2024-04-25T10:00:00Z",
                "updated_at": "2024-04-25T11:00:00Z",
                "max_orders": 5,
                "current_number_orders": 2,
                "latitude": "40.7128",
                "longitude": "-74.0060",
                "is_working": 1,
                "orders_count": 5,
                "completed_orders": 3,
                "active_comision": 5.5,
                "reserve_complete": 0,
                "rate_active_carriers": 80,
                "backpack_code": "BP123",
                "class_id": 4
            },
            {
                "id": 2,
                "is_active": 1,
                "status": 1,
                "device_token": "def456mno",
                "user_id": 49275,
                "created_at": "2024-04-25T12:00:00Z",
                "updated_at": "2024-04-25T12:30:00Z",
                "max_orders": 3,
                "current_number_orders": 1,
                "latitude": "34.0522",
                "longitude": "-118.2437",
                "is_working": 1,
                "orders_count": 2,
                "completed_orders": 2,
                "active_comision": 3.0,
                "reserve_complete": 1,
                "rate_active_carriers": 90,
                "backpack_code": "BP456",
                "class_id": 5
            },
            {
                "id": 3,
                "is_active": 1,
                "status": 1,
                "device_token": "ghi789pqr",
                "user_id": 68441,
                "created_at": "2024-04-25T14:00:00Z",
                "updated_at": "2024-04-25T15:00:00Z",
                "max_orders": 4,
                "current_number_orders": 3,
                "latitude": "51.5074",
                "longitude": "-0.1278",
                "is_working": 1,
                "orders_count": 8,
                "completed_orders": 5,
                "active_comision": 6.0,
                "reserve_complete": 1,
                "rate_active_carriers": 95,
                "backpack_code": "BP789",
                "class_id": 6
            }
        ]

    async def get_available_drivers_profile(self) -> List[DriverProfile]:
        return [DriverProfile(**driver) for driver in self.profile_drivers]

    async def get_busy_drivers_profile(self) -> List[DriverProfile]:
        pass
