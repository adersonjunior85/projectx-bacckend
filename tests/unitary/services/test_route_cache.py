import json
from unittest.mock import MagicMock, patch

import pytest

from app.infra.clients.exceptions import (
    GetRouteError,
    KeyExistsError,
    SaveRouteError,
    SetExpirationError,
)
from app.services.route_cache import RouteCache


@pytest.fixture
def mock_redis_client():
    return MagicMock()


@pytest.fixture
def route_cache(mock_redis_client):
    with patch("app.services.route_cache.client_redis", mock_redis_client):
        yield RouteCache()


def test_get_route_success(route_cache, mock_redis_client):
    mock_route = {
        "transaction_route_id": "123456",
        "routes": [{"total_toll_value": 100}],
    }

    mock_redis_client.exists.return_value = True
    mock_redis_client.get.return_value = json.dumps(mock_route)

    route = route_cache.get_route("123456")

    mock_redis_client.get.assert_called_once_with("123456")

    assert route == mock_route


def test_get_route_not_found(route_cache, mock_redis_client):
    mock_redis_client.exists.return_value = False

    with pytest.raises(Exception, match="Route not found or expired."):
        route_cache.get_route("123456")


def test_get_route_error(route_cache, mock_redis_client):
    mock_redis_client.exists.return_value = True
    mock_redis_client.get.side_effect = Exception("Error getting route")

    with pytest.raises(GetRouteError):
        route_cache.get_route("123456")


def test_set_expiration_error(route_cache, mock_redis_client):
    mock_redis_client.expire.side_effect = Exception(
        "Error setting expiration"
    )

    with pytest.raises(SetExpirationError):
        route_cache._set_expiration("123456")


def test_key_exists_error(route_cache, mock_redis_client):
    mock_redis_client.exists.side_effect = Exception(
        "Error checking key exists"
    )

    with pytest.raises(KeyExistsError):
        route_cache._exists("123456")


def test_save_route_error(route_cache, mock_redis_client):
    mock_route = MagicMock()
    mock_route.transaction_route_id = "123456"
    mock_route.dict.return_value = {
        "transaction_route_id": "123456",
        "routes": [{"total_toll_value": 100}],
    }

    mock_redis_client.set.side_effect = Exception("Error saving route")

    with pytest.raises(SaveRouteError):
        route_cache.save(mock_route)
