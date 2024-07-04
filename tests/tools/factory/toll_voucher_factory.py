from faker import Faker

from app.models.toll_voucher import TollVoucherCreate
from tests.tools.factory.address_factory import AddressCreateFactory
from tests.tools.factory.shipper_factory import ShipperCreateFactory
from tests.tools.factory.vehicle_factory import VehicleCreateFactory

faker = Faker(locale="pt_BR")


class TollVoucherCreateFactory:
    @staticmethod
    def build(params: dict = None) -> TollVoucherCreate:
        if not params:
            params = {}

        return TollVoucherCreate(
            code=params.get(
                "code", str(faker.random_int(min=10000, max=3000000))
            ),
            ciot_code=params.get(
                "ciot_code",
                str(faker.random_int(min=10000, max=3000000)),
            ),
            identifier=params.get(
                "identifier", str(faker.random_int(min=10000, max=3000000))
            ),
            start_date=params.get("start_date", faker.date_time_this_year()),
            end_date=params.get("end_date", faker.date_time_this_year()),
            value=params.get("value", faker.random_int(min=1000, max=100000)),
            is_round_trip=params.get("is_round_trip", False),
            status=params.get("status", "emitted"),
            note=params.get("note", "Random note"),
            origin=AddressCreateFactory.build(params.get("origin")),
            destination=AddressCreateFactory.build(params.get("destination")),
            vehicle=VehicleCreateFactory.build(params.get("vehicle")),
            shipper=ShipperCreateFactory.build(params.get("shipper")),
        )
