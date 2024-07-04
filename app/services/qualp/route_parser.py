from typing import Any, Dict

from pydantic import BaseModel, Field, model_validator


class Tariff(BaseModel):
    value: float = Field()
    value_per_axis: float | None = Field(
        default=0.0, serialization_alias="value_per_axis"
    )

    @model_validator(mode="before")
    def extract_value(cls, values: Dict[str, Any]):
        if isinstance(values.get("value"), dict):
            key, value = list(values["value"].items())[0]
            values["value"] = value
            values["value_per_axis"] = round(float(value) / float(key), 2)
        return values


class Distance(BaseModel):
    texto: str = Field(serialization_alias="text")
    valor: int = Field(serialization_alias="value")


class Duration(BaseModel):
    texto: str = Field(serialization_alias="text")
    valor: int = Field(serialization_alias="value")


class Toll(BaseModel):
    codigo_antt: str = Field(serialization_alias="antt_code")
    codigo_integracao_sem_parar: int = Field(
        serialization_alias="sem_parar_integration_code",
    )
    codigo_conectcar: int = Field(serialization_alias="conectcar_code")
    codigo_integracao_veloe: int = Field(
        serialization_alias="veloe_integration_code",
    )
    concessionaria: str = Field(serialization_alias="concessionaire")
    nome: str = Field(serialization_alias="name")
    uf: str = Field(serialization_alias="state")
    municipio: str = Field(serialization_alias="city")
    codigo_ibge: str = Field(serialization_alias="ibge_code")
    rodovia: str = Field(serialization_alias="highway")
    km: str = Field()
    tarifa: Tariff = Field(serialization_alias="tariff")
    special_toll: bool = Field()
    porcentagem_fim_semana: int = Field(
        serialization_alias="weekend_percentage",
    )
    porcentagem_tag: int = Field(serialization_alias="tag_percentage")
    porcentagem_tag_arredondamento: str = Field(
        serialization_alias="tag_rounding_percentage",
    )
    latitude: float = Field()
    longitude: float = Field()

    @model_validator(mode="before")
    def convert_tariff(cls, values: Dict[str, Any]):
        if isinstance(values.get("tarifa"), dict):
            values["tarifa"] = Tariff(value=values["tarifa"])
        return values


class Route(BaseModel):
    distancia: Distance = Field(serialization_alias="distance")
    duracao: Duration = Field(serialization_alias="duration")
    endereco_inicio: str = Field(serialization_alias="start_address")
    endereco_fim: str = Field(serialization_alias="end_address")
    coordenada_inicio: str = Field(serialization_alias="start_coordinates")
    coordenada_fim: str = Field(serialization_alias="end_coordinates")
    tolls: list[Toll] = Field(alias="pedagios", serialization_alias="tolls")
    polilinha_codificada: str = Field(serialization_alias="encoded_polyline")
    total_toll_value: float = Field(default=0.0)
    total_tolls: int = Field(default=0)

    @model_validator(mode="after")
    def validate_model(self):
        self.total_toll_value = sum(toll.tarifa.value for toll in self.tolls)
        self.total_tolls = len(self.tolls)

        return self


class RouteResponse(BaseModel):
    rotas: list[Route] = Field(serialization_alias="routes")
    locais: list[str] = Field(serialization_alias="locations")
    id_transacao: int = Field(serialization_alias="transaction_id")
    roteador_selecionado: str = Field(serialization_alias="selected_router")
    calcular_volta: bool = Field(serialization_alias="calculate_return")
    otimizar_rota: bool = Field(serialization_alias="optimize_route")
    provider: str = Field()

    class Config:
        populate_by_name = True
