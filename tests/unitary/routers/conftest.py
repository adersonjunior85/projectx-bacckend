from unittest.mock import AsyncMock, patch

import pytest

from app.services.geo_api import GeoApiService


@pytest.fixture
def mock_geo_api_service():
    service = AsyncMock(GeoApiService)
    with patch("app.routers.v1.route.GeoApiService", return_value=service):
        yield service


@pytest.fixture
def mock_route_data():
    return {
        "is_round_trip": False,
        "return_to_same_place": False,
        "provider": "semparar",
        "start_date": "27/05/2024",
        "end_date": "27/05/2024",
        "persist_route": False,
        "vehicle_category": "2",
        "places": [
            {
                "city": "São paulo",
                "point": [],
                "state": "SP",
                "country": "BRA",
            },
            {
                "city": "São paulo",
                "point": [],
                "state": "atibaia",
                "country": "BRA",
            },
            {
                "city": "Ribeirão preto",
                "point": [],
                "state": "SP",
                "country": "BRA",
            },
        ],
    }


@pytest.fixture
def mock_response_data():
    return {"route": ["locationA", "locationB"]}
