import pytest
from decouple import config
from app.core.repositories.drivers_profile_mysql_repo_impl import DriversProfileMySQLRepoImpl


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
def test_get_available_drivers_profile(db_config):
    drivers_profile_repo = DriversProfileMySQLRepoImpl(db_config)
    drivers = drivers_profile_repo.get_available_drivers_profile()
    assert len(drivers) > 0


@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
def test_get_busy_drivers_profile(db_config):
    drivers_profile_repo = DriversProfileMySQLRepoImpl(db_config)
    drivers = drivers_profile_repo.get_busy_drivers_profile()
    assert len(drivers) > 0

@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
def test_get_busy_drivers_profile_ibarra_city(db_config):
    drivers_profile_repo = DriversProfileMySQLRepoImpl(db_config)
    drivers =  drivers_profile_repo.get_available_drivers_profile_by_city(1)
    assert len(drivers) > 0