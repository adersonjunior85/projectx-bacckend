from datetime import datetime
from uuid import UUID

from sqlmodel import Field, SQLModel

from app.enums.toll_voucher_providers import TollVoucherProviders
from app.enums.toll_voucher_status_types import TollVoucherStatusTypes
from app.models.address import AddressCreate, AddressRead
from app.models.route import RouteCreate
from app.models.shipper import ShipperCreate, ShipperRead
from app.models.vehicle import VehicleCreate, VehicleRead


class TollVoucherBase(SQLModel):
    identifier: str | None = Field(
        default=None, description="Identificador do Vale Pedágio"
    )
    ciot_code: str | None = Field(
        default=None, description="Código do CIOT correspondente"
    )
    note: str | None = Field(
        default=None, description="Observação", max_length=250
    )


class TollVoucherCreate(TollVoucherBase):
    origin: AddressCreate = Field()
    destination: AddressCreate = Field()
    vehicle: VehicleCreate = Field()
    shipper: ShipperCreate = Field()


class TollVoucherEmit(TollVoucherBase):
    origin: AddressCreate = Field()
    destination: AddressCreate = Field()
    route: RouteCreate = Field()
    vehicle: VehicleCreate = Field()
    shipper: ShipperCreate = Field()


class TollVoucherRead(TollVoucherBase):
    id: UUID
    status: TollVoucherStatusTypes
    origin: AddressRead
    destination: AddressRead
    vehicle: VehicleRead
    shipper: ShipperRead


class TollVoucherListRead(SQLModel):
    id: UUID
    identifier: str | None
    code: str | None
    status: TollVoucherStatusTypes | None
    emission_date: datetime | None
    vehicle_plate: str
    provider: TollVoucherProviders


class TollVoucherUpdate(SQLModel):
    id: UUID
    origin: AddressCreate = Field()
    destination: AddressCreate = Field()
    vehicle: VehicleCreate = Field()
    shipper: ShipperCreate = Field()


class TollVoucherDelete(SQLModel):
    pass
