from unittest.mock import AsyncMock, patch

import httpx
import pytest

from app.infra.clients.exceptions import RouteRequestFailed
from app.infra.clients.geo_api import GeoApiClient


@pytest.fixture
def geo_api_client():
    return GeoApiClient()


@pytest.fixture
def mock_settings():
    with patch("app.infra.clients.geo_api.settings") as mock:
        mock.GEO_API = "http://mock-api.com"
        mock.TIMEOUT = 5.0
        mock.TRIES = 3
        mock.DELAY = 1
        yield mock


@pytest.fixture
def mock_response_data():
    return {"route": ["locationA", "locationB"]}


def create_mock_response(status_code, json_data):
    request = httpx.Request("POST", "http://mock-api.com/v1/vpo/route")
    response = httpx.Response(status_code, request=request)
    response._content = httpx._content.json_dumps(json_data).encode("utf-8")
    return response


@pytest.mark.asyncio
async def test_generate_route_success(geo_api_client, mock_response_data):
    mock_response = create_mock_response(200, mock_response_data)
    with patch.object(
        httpx.AsyncClient, "post", AsyncMock(return_value=mock_response)
    ):
        result = await geo_api_client.generate_route(payload={"key": "value"})
        assert result == mock_response_data


@pytest.mark.asyncio
async def test_generate_route_http_status_error(geo_api_client):
    request = httpx.Request("POST", "http://mock-api.com/v1/vpo/route")
    mock_response = httpx.Response(status_code=400, request=request)
    async_mock_post = AsyncMock(
        side_effect=httpx.HTTPStatusError(
            "Error", request=request, response=mock_response
        )
    )

    with patch.object(
        httpx.AsyncClient, "post", async_mock_post
    ), pytest.raises(RouteRequestFailed):
        await geo_api_client.generate_route(payload={"key": "value"})


@pytest.mark.asyncio
async def test_generate_route_request_error(geo_api_client):
    request = httpx.Request("POST", "http://mock-api.com/v1/vpo/route")
    async_mock_post = AsyncMock(
        side_effect=httpx.RequestError("Error", request=request)
    )

    with patch.object(
        httpx.AsyncClient, "post", async_mock_post
    ), pytest.raises(RouteRequestFailed):
        await geo_api_client.generate_route(payload={"key": "value"})
