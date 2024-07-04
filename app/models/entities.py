from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship

from app.enums.toll_voucher_status_types import TollVoucherStatusTypes
from app.models.address import AddressBase
from app.models.route import RouteBase, TollPlazaBase


class Address(AddressBase, table=True):
    __tablename__ = "addresses"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
