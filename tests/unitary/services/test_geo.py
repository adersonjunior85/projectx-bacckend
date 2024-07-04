from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.services.geo_api import GeoApiService
from app.services.qualp.route_parser import RouteResponse


@pytest.fixture
def geo_api_service():
    with patch(
        "app.services.geo_api.GeoApiClient", autospec=True
    ) as mock_geo_client, patch(
        "app.services.geo_api.RouteCache", autospec=True
    ) as mock_route_cache:
        service = GeoApiService()
        service.client = mock_geo_client.return_value
        service.route_cache = mock_route_cache.return_value
        yield service


@pytest.fixture
def mock_response_data_long():
    return {
        "rotas": [
            {
                "distancia": {"texto": "357 km", "valor": 357},
                "distancia_nao_pavimentada": {
                    "texto": "0 km",
                    "valor": 0,
                    "percentual_texto": "0%",
                    "percentual_valor": 0,
                },
                "duracao": {"texto": "03:45:37", "valor": 13537},
                "endereco_inicio": "-23.5557714,-46.6395571",
                "endereco_fim": "-21.1694018,-47.8110855",
                "coordenada_inicio": "-23.5557714,-46.6395571",
                "coordenada_fim": "-21.1694018,-47.8110855",
                "pedagios": [
                    {
                        "id_api": "1714",
                        "codigo_antt": "35013810666000101",
                        "codigo_integracao_sem_parar": 207,
                        "codigo_integracao_sem_parar_praca": 412,
                        "sentido_integracao_sem_parar": "N",
                        "direcao_integracao_sem_parar": "C",
                        "codigo_conectcar": 611,
                        "sentido_conectcar": "A",
                        "codigo_integracao_veloe": 110,
                        "codigo_integracao_veloe_concessionaria": 6,
                        "sentido_integracao_veloe": "S",
                        "codigo_integracao_movemais": 35013810666000101,
                        "codigo_integracao_movemais_praca": 6180000600001,
                        "sentido_integracao_movemais": "A",
                        "codigo_integracao_dclogg": 289,
                        "sentido_integracao_dclogg": "N",
                        "concessionaria": "FERNÃO DIAS",
                        "concessionaria_contato": "(35) 3449-6600 / 0800",
                        "nome": "P1-Mairiporâ",
                        "uf": "SP",
                        "municipio": "Mairiporã",
                        "codigo_ibge": "3528502",
                        "rodovia": "BR-381",
                        "km": "65.700",
                        "tarifa": {"5": 14.5},
                        "special_toll": False,
                        "porcentagem_fim_semana": 0,
                        "porcentagem_tag": 0,
                        "porcentagem_tag_arredondamento": "cima",
                        "latitude": -23.322304,
                        "longitude": -46.581162,
                        "p_index": 782,
                    }
                ],
                "polilinha_codificada": "@nFkL",
            }
        ],
        "locais": [
            "-23.5557714,-46.6395571",
            "-23.1155873,-46.5532067",
            "-21.1694018,-47.8110855",
        ],
        "id_transacao": 57929161,
        "roteador_selecionado": "qualp",
        "calcular_volta": False,
        "otimizar_rota": False,
        "provider": "Qualp",
        "cached": True,
        "fuel_usage": 0.0,
        "fuel_usage_unit": "liters",
        "fuel_cost": 0.0,
        "fuel_cost_unit": "R$",
        "total_cost": 0.0,
    }


@pytest.mark.asyncio
async def test_generate_route_without_persistence(
    geo_api_service, mock_response_data_long
):
    mock_params = MagicMock()
    mock_params.dict.return_value = {"key": "value"}

    async_mock_generate_route = AsyncMock(return_value=mock_response_data_long)

    with patch.object(
        geo_api_service.client, "generate_route", async_mock_generate_route
    ), patch(
        "app.services.geo_api.RouteResponse", autospec=True
    ) as mock_route_response:
        mock_route_response.return_value = RouteResponse(
            **mock_response_data_long
        )
        result = await geo_api_service.generate_route(params=mock_params)
        assert result == mock_route_response.return_value


@pytest.mark.asyncio
async def test_generate_route_with_persistence(
    geo_api_service, mock_response_data_long
):
    mock_params = MagicMock()
    mock_params.dict.return_value = {"key": "value", "persist_route": True}

    async_mock_generate_route = AsyncMock(return_value=mock_response_data_long)

    with patch.object(
        geo_api_service.client, "generate_route", async_mock_generate_route
    ), patch(
        "app.services.geo_api.RouteResponse", autospec=True
    ) as mock_route_response, patch.object(
        geo_api_service.route_cache, "save", return_value=("route_id", 100.0)
    ):
        mock_route_response.return_value = RouteResponse(
            **mock_response_data_long
        )

        result = await geo_api_service.generate_route(params=mock_params)

        assert result == {
            "transaction_route_id": "route_id",
            "tolls_gross_amount": 100.0,
        }


def test_persist_route(geo_api_service):
    mock_parsed_data = MagicMock()
    geo_api_service.route_cache.save.return_value = ("route_id", 100.0)

    result = geo_api_service.persist_route(parsed_data=mock_parsed_data)
    assert result == {
        "transaction_route_id": "route_id",
        "tolls_gross_amount": 100.0,
    }
