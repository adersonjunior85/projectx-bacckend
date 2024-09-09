from uuid import UUID, uuid4

from sqlmodel import Field

from app.models.address import AddressBase


class Address(AddressBase, table=True):
    __tablename__ = "addresses"

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
