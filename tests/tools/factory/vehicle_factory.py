from faker import Faker

from app.models.vehicle import VehicleCreate

faker = Faker(locale="pt_BR")


class VehicleCreateFactory:
    def __init__(self):
        pass

    @staticmethod
    def build(params: dict = None) -> VehicleCreate:
        if not params:
            params = {}

        return VehicleCreate(
            name=params.get("name", faker.name()),
            plate=params.get("plate", "AUS3C32"),
            category=params.get("category", 1),
            toll_voucher_provider=params.get(
                "toll_voucher_provider", "sem_parar"
            ),
            tag=params.get("tag", 132098),
        )
