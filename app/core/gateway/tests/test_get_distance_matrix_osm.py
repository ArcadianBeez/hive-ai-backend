import pytest
from decouple import config

from app.core.gateway.distance_matrix_osm_impl import DistanceMatrixOsmImpl


@pytest.mark.skipif(config("LIVE_TESTS", cast=bool, default=False) is False, reason="Live tests are disabled")
@pytest.mark.asyncio
async def test_get_distance_matrix_osm_impl():
    osm_gateway = DistanceMatrixOsmImpl(config("OSM_BASE_URL"))
    origins = [
        "-78.130226,0.342812",# Pilanqui park
        "-78.135704,0.349093",#Ceviches Rumi Imbauto
        "-78.118469,0.350050"#san Agustin
    ]
    destinations = [
        "-78.135601,0.345482",#kfc la plaza
        #"-78.124709,0.348028",#kfc gran aki
        #"-78.121010,0.349399"#rico mote
    ]
    response = await osm_gateway.get_distance_matrix(origins, destinations)
    assert response == [1393.2, 489.3, 2484.5]
