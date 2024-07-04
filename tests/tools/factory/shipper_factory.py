from faker import Faker

from app.models.shipper import ShipperCreate

faker = Faker(locale="pt_BR")


class ShipperCreateFactory:
    def __init__(self):
        pass

    @staticmethod
    def build(params: dict = None) -> ShipperCreate:
        if not params:
            params = {}

        return ShipperCreate(
            name=params.get("name", faker.name()),
            document=params.get("document", faker.cpf()),
        )
