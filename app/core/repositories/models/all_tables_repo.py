import abc

from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List


class ResponseHiveData(BaseModel):
    id: int = Field(None, alias='id')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class HiveQueries(abc.ABC):
    @abc.abstractmethod
    async def fetch_by_query(self) -> List[ResponseHiveData]:
        pass
