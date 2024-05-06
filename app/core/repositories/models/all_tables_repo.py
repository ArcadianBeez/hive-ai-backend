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

class HiveQueriesRepo(abc.ABC):
    @abc.abstractmethod
    async def fetch_by_query(self, query: str) -> List[ResponseHiveData]:
        pass
