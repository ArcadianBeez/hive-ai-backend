import firebase_admin
import inject
import pytest
from decouple import config
from firebase_admin import credentials, db

from app.core.gateway.distance_matrix_osm_impl import DistanceMatrixOsmImpl, DistanceMatrixGateway
from app.core.repositories.drivers_location_firebase_repo_impl import DriversLocationRepoFirebaseImpl
from app.core.repositories.models.drivers_location_repo import DriversLocationRepo
from app.core.repositories.models.drivers_profile_repo import DriversProfileRepo
from app.core.repositories.models.orders_repo import OrdersRepo
from app.logic.assigner.assign_free_orders import AssignFreeOrdersUCImpl
from app.logic.assigner.mocks.drivers_profile_repo_mock_impl import DriversProfileRepoMockImpl
from app.logic.assigner.mocks.orders_repo_mock_impl import OrdersRepoMockImpl


def my_config(binder):
    config_db = {
        "host": config("DB_HOST"),
        "user": config("DB_USER"),
        "password": config("DB_PASSWORD"),
        "database": config("DB_NAME"),
        "charset": 'utf8mb4'
    }

    binder.bind(OrdersRepo, OrdersRepoMockImpl())

    cred = credentials.Certificate(config("FIREBASE_CREDS_PATH"))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://phoenix-247205.firebaseio.com/'
    })
    ref = db.reference('locationsDrivers')
    binder.bind(DriversLocationRepo, DriversLocationRepoFirebaseImpl(ref))
    binder.bind(DriversProfileRepo, DriversProfileRepoMockImpl())
    binder.bind(DistanceMatrixGateway, DistanceMatrixOsmImpl(config("OSM_BASE_URL")))


@pytest.fixture
def inject_live_config():
    inject.clear_and_configure(my_config)


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_assign_free_orders(inject_live_config):
    uc = AssignFreeOrdersUCImpl()
    response = await uc.execute(1)
    assert response == "Assignments Complete"
