from faker import Faker

from app.models.address import AddressCreate

faker = Faker(locale="pt_BR")


class AddressCreateFactory:
    def __init__(self):
        pass

    @staticmethod
    def build(params: dict = None) -> AddressCreate:
        if not params:
            params = {}

        return AddressCreate(
            country=params.get("country", None),
            state_acronym=params.get("state_acronym", "SP"),
            neighborhood=params.get("neighborhood", None),
            address=params.get("address", None),
            number=params.get("number", None),
            display_name=params.get("display_name", "São Paulo SP"),
            point=params.get("point", None),
            is_precise_location=params.get("is_precise_location", True),
            area_code=params.get("area_code", 11),
            city=params.get("city", faker.city()),
            state=params.get("state", faker.state()),
            zip_code=params.get("zip_code", faker.postcode(formatted=False)),
        )
