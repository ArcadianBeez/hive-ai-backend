import inject
import pytest
from decouple import config

from app.core.gateway.open_ai_impl import OpenAIGateway, OpenAIGatewayImpl
from app.core.repositories.all_tables import HiveQueriesRepoImpl
from app.core.repositories.models.all_tables_repo import HiveQueriesRepo
from app.logic.query_generator_ai.index import QueryGeneratorAIUC, QueryGeneratorAIUCImpl


def my_config(binder):
    config_db = {
        "host": config("DB_HOST"),
        "user": config("DB_USER"),
        "password": config("DB_PASSWORD"),
        "database": config("DB_NAME"),
        "charset": 'utf8mb4'
    }

    binder.bind(HiveQueriesRepo, HiveQueriesRepoImpl(config_db))
    binder.bind(OpenAIGateway, OpenAIGatewayImpl(api_key=config("OPENAI_API_KEY")))


@pytest.fixture
def inject_live_config():
    inject.clear_and_configure(my_config)


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_generate_query(inject_live_config):
    query_generator = QueryGeneratorAIUCImpl()
    instruction = "Cuales son las ventas de hoy?"
    generated_query = await query_generator.execute(instruction)
    assert generated_query is not None  # Or other appropriate assertions

