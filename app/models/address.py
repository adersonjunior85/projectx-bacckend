from uuid import UUID

from sqlmodel import JSON, Field, SQLModel


class AddressBase(SQLModel):
    country: str | None = Field(default="Brasil", description="País")
    state_acronym: str | None = Field(
        default=None, description="Acrônimo do estado"
    )
    state: str = Field(description="Estado")
    zip_code: str | None = Field(default=None, description="CEP")
    city: str = Field(description="Cidade")
    neighborhood: str | None = Field(default=None, description="Bairro")
    address: str | None = Field(default=None, description="Endereço")
    number: str | None = Field(default=None, description="Número")
    display_name: str = Field(description="")
    point: tuple[float, float] | None = Field(
        default=None,
        sa_type=JSON,
        description="Coordenadas do endereço (latitude,longitude)",
    )
    is_precise_location: bool | None = Field(default=None, description="")
    area_code: int | None = Field(default=None, description="Código de área")


class AddressCreate(AddressBase):
    pass


class AddressRead(AddressBase):
    id: UUID
