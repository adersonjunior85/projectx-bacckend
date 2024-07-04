import pytest


@pytest.mark.asyncio
async def test_generate_route_success(
    client, mock_geo_api_service, mock_route_data, mock_response_data
):
    mock_geo_api_service.generate_route.return_value = mock_response_data

    response = client.post("/v1/routes", json=mock_route_data)

    assert response.status_code == 200
    assert response.json() == mock_response_data
