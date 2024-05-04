import json

import firebase_admin
import pytest
from decouple import config
from firebase_admin import credentials, db

from app.core.repositories.drivers_location_firebase_repo_impl import DriversLocationRepoFirebaseImpl

@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_driver_locations():
    cred = credentials.Certificate(json.loads(config("FILE_SIGNER_CREDS").replace("'", '"')))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://phoenix-247205.firebaseio.com/'
    })
    ref = db.reference('locationsDrivers')
    drivers_locations_repo = DriversLocationRepoFirebaseImpl(ref)
    drivers = drivers_locations_repo.get_drivers_location()
    assert len(drivers) > 0

@pytest.mark.skipif(not config("LIVE_TESTS", default=False, cast=bool), reason="Integration tests are disabled")
@pytest.mark.asyncio
async def test_get_driver_location_by_id():
    cred = credentials.Certificate(json.loads(config("FILE_SIGNER_CREDS").replace("'", '"')))
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://phoenix-247205.firebaseio.com/'
    })
    ref = db.reference('locationsDrivers')
    drivers_locations_repo = DriversLocationRepoFirebaseImpl(ref)
    driver = await drivers_locations_repo.get_driver_location_by_id("65983")
    assert driver is not None
