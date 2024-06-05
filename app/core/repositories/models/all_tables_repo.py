import abc
from pydantic import BaseModel, Field
from typing import Optional, List


from pydantic import BaseModel, Field

default_actions = [
    {"label": "Detallar", "path": "/more_info", "type": ""},
    {"label": "Exportar", "path": "/export", "type": ""},
    {"label": "Graficos", "path": "/graphics", "type": ""},
]


class ResponseHiveData(BaseModel):
    id: int = Field(None, alias='id')
    actions: Optional[List[dict]] = Field(default_actions, alias='actions')

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
