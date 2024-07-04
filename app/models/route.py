from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import field_validator
from sqlmodel import JSON, Field, SQLModel

from app.enums.toll_voucher_providers import TollVoucherProvidersStrEnum


class TollPlazaBase(SQLModel):
    axle_value: int = Field(description="Valor por eixo (base x100)")
    value: int = Field(description="Valor total (base x100)")
    address: str = Field(description="Endereço da praça")
    name: str = Field(description="Nome da praça")
    toll_id: str = Field(description="")
    toll_provider_id: int = Field(description="")
    point: tuple[float, float] | None = Field(
        default=None,
        sa_type=JSON,
        description="Coordenadas do endereço (latitude,longitude)",
    )
    antt_code: str = Field()
    weekend_percentage: int = Field(description="")
    sem_parar_code: int = Field(description="")
    conectcar_code: int = Field(description="")
    gross_value: int = Field(description="Valor bruto (base x100)")


class RouteBase(SQLModel):
    origin: str = Field(description="Endereço de origem")
    destination: str = Field(description="Endereço de destino")
    start_date: datetime = Field(description="Data de início da viagem")
    end_date: datetime = Field(description="Data de fim da viagem")
    is_round_trip: bool = Field()


class Place(SQLModel):
    toll_date: str | None = Field(default=None, description="Data da viagem")
    state: str = Field(description="Estado")
    country: str = Field(description="País")
    city: str = Field(description="Cidade")
    coordinates: List[float] | None = Field(
        default=None, description="Pontos de latitude/longitude das cidades"
    )


class RouteRequestBase(SQLModel):
    persist_route: bool | None = Field(
        default=False, description="Retorna a rota otimizada"
    )
    vehicle_category: str = Field(description="Categoria do veículo")
    provider: TollVoucherProvidersStrEnum = Field(
        description="Provedor do Vale Pedágio"
    )
    is_round_trip: bool | None = Field(
        default=False, description="Roteiriza ida e volta"
    )
    return_to_same_place: bool | None = Field(
        default=False, description="Retorne pelo mesmo caminho"
    )
    places: List[Place] = Field(description="Pontos de parada")
    start_date: str | None = Field(
        default=None, description="Data de início da viagem"
    )
    end_date: str | None = Field(
        default=None, description="Data de término da viagem"
    )
    raw: bool | None = Field(default=True, description="Retorna dados brutos")

    @field_validator("places")
    def validate_places(cls, places, values):
        is_round_trip = values.data.get("is_round_trip")
        return_to_same_place = values.data.get("return_to_same_place")

        if is_round_trip and return_to_same_place:
            places.reverse()
        elif is_round_trip:
            return [places[-1], places[0]]

        return places


class RouteCreate(RouteBase):
    toll_plazas: list[TollPlazaBase] = Field(
        description="Praças de pedágio na rota"
    )


class RouteRead(RouteBase):
    id: UUID = Field()
