import pytest
from decouple import config
from app.core.repositories.orders_mysql_repo import OrderMySQLRepoImpl


@pytest.fixture()
def db_config():
    return {
        "host": config("DB_HOST"),
        "user": config("DB_USER"),
        "password": config("DB_PASSWORD"),
        "database": config("DB_NAME"),
        "charset": 'utf8mb4'
    }


@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_free_fast_orders(db_config):
    orders_repo = OrderMySQLRepoImpl(db_config)
    orders = await orders_repo.get_fast_orders_without_driver()
    print("Órdenes obtenidas:", orders)
    assert len(orders) > 0


@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_free_busy_orders(db_config):
    orders_repo = OrderMySQLRepoImpl(db_config)
    orders =await orders_repo.get_slow_orders_without_driver()
    assert len(orders) > 0


@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_free_fast_orders_without_ibarra_city(db_config):
    orders_repo = OrderMySQLRepoImpl(db_config)
    orders = await orders_repo.get_fast_orders_without_driver_by_city(1)
    assert len(orders) > 0

@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_free_fast_orders_without_atuntaqui_city(db_config):
    orders_repo = OrderMySQLRepoImpl(db_config)
    orders = await orders_repo.get_fast_orders_without_driver_by_city(2)
    assert len(orders) > 0

@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_free_fast_orders_without_atuntaqui_city(db_config):
    orders_repo = OrderMySQLRepoImpl(db_config)
    orders = await orders_repo.get_slow_orders_without_driver_by_city(1)
    assert len(orders) > 0

