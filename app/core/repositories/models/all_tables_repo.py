import abc
from pydantic import BaseModel, Field
from typing import Optional, List

from pydantic import BaseModel, Field


class ResponseHiveData(BaseModel):
    id: int = Field(None, alias='id')

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        extra = "allow"

    def dict(self, **kwargs):
        return super().dict(exclude={'id'}, **kwargs)

    def json(self, **kwargs):
        return super().json(exclude={'id'}, **kwargs)


class HiveQueriesRepo(abc.ABC):
    @abc.abstractmethod
    async def fetch_by_query(self, query: str) -> List[ResponseHiveData]:
        pass
