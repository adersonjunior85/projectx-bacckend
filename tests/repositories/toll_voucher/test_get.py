from uuid import uuid4

import pytest

from app.repositories.toll_voucher import TollVoucherRepository
from tests.tools.factory.toll_voucher_factory import TollVoucherCreateFactory


class TestTollVoucherRepositoryGet:
    def test_success(self, session):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build()
        created_toll_voucher = repository.create(toll_voucher_create)

        retrieved_toll_voucher = repository.get_by_id(created_toll_voucher.id)

        assert retrieved_toll_voucher.id == created_toll_voucher.id
        assert retrieved_toll_voucher.status == created_toll_voucher.status

    def test_get_addresses_success(self, session):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build()
        created_toll_voucher = repository.create(toll_voucher_create)
        retrieved_toll_voucher = repository.get_by_id(created_toll_voucher.id)

        origin = toll_voucher_create.origin
        destination = toll_voucher_create.destination
        origin_response = retrieved_toll_voucher.origin
        destination_response = retrieved_toll_voucher.destination

        assert origin.city == origin_response.city
        assert origin.zip_code == origin_response.zip_code
        assert destination.city == destination_response.city
        assert destination.zip_code == destination_response.zip_code
        ...

    def test_get_vehicle_success(self, session):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build()
        vehicle = toll_voucher_create.vehicle
        created_toll_voucher = repository.create(toll_voucher_create)

        vehicle_response = repository.get_by_id(
            created_toll_voucher.id
        ).vehicle

        assert vehicle.name == vehicle_response.name
        assert vehicle.plate == vehicle_response.plate
        assert vehicle.category == vehicle_response.category

        ...

    def test_get_shipper_success(self, session):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build()
        shipper = toll_voucher_create.shipper
        created_toll_voucher = repository.create(toll_voucher_create)

        shipper_response = repository.get_by_id(
            created_toll_voucher.id
        ).shipper

        assert shipper.name == shipper_response.name
        assert shipper.document == shipper_response.document

        ...

    def test_non_existing_id_error(self, session):
        repository = TollVoucherRepository(session)
        non_existing_id = uuid4()  # Assumindo que este ID não existe

        with pytest.raises(AttributeError):
            repository.get_by_id(non_existing_id)
