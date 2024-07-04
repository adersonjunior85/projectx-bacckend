from uuid import UUID

from sqlmodel import Field, SQLModel

from app.enums.toll_voucher_providers import TollVoucherProviders


class VehicleBase(SQLModel):
    name: str | None = Field(
        default=None, description="Nome fantasia do veículo"
    )
    plate: str = Field(description="Placa do veículo")
    category: int = Field(description="Categoria do veículo")
    toll_voucher_provider: TollVoucherProviders = Field(
        description="Provedor do Vale Pedágio"
    )
    tag: int = Field(description="Tag de pedágio do veículo")


class VehicleCreate(VehicleBase):
    pass


class VehicleRead(VehicleBase):
    id: UUID
