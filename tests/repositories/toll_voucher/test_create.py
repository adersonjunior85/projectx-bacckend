import pytest
from pydantic_core import ValidationError

from app.enums.toll_voucher_status_types import TollVoucherStatusTypes
from app.repositories.toll_voucher import TollVoucherRepository
from tests.tools.factory.toll_voucher_factory import TollVoucherCreateFactory


class TestTollVoucherRepositoryCreate:
    def test_success(self, session):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build()

        response = repository.create(toll_voucher_create)

        assert response.id is not None
        assert response.status is TollVoucherStatusTypes.DRAFT

    @pytest.mark.parametrize(
        "optional_field", ["note", "identifier", "ciot_code"]
    )
    def test_without_optional_fields_success(self, session, optional_field):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build(
            params={optional_field: None}
        )

        response = repository.create(toll_voucher_create)

        assert response.id is not None
        assert response.status is TollVoucherStatusTypes.DRAFT

    @pytest.mark.parametrize(
        "field, invalid_value, error_type",
        [
            pytest.param("note", -321, "string_type", id="string_type1"),
            pytest.param("note", True, "string_type", id="string_type2"),
            pytest.param(
                "ciot_code", 312.52, "string_type", id="string_type3"
            ),
            pytest.param("ciot_code", False, "string_type", id="string_type4"),
            pytest.param("identifier", True, "string_type", id="string_type5"),
            pytest.param(
                "identifier", 43210, "string_type", id="string_type6"
            ),
        ],
    )
    def test_with_invalid_fields_error(self, field, invalid_value, error_type):
        pattern = rf"\[type={error_type},.*\]"

        with pytest.raises(ValidationError, match=pattern):
            TollVoucherCreateFactory.build({field: invalid_value})

    # Testes de endereço
    @pytest.mark.parametrize(
        "field, invalid_value, error_type",
        [
            pytest.param("city", -321, "string_type", id="negative-int"),
            pytest.param("city", 500, "string_type", id="int"),
            pytest.param("state", 312.52, "string_type", id="float"),
            pytest.param("country", 312231, "string_type", id="big-int"),
            pytest.param("zip_code", True, "string_type", id="bool"),
        ],
    )
    def test_with_invalid_address_fields_error(
        self, field, invalid_value, error_type
    ):
        pattern = rf"\[type={error_type},.*\]"

        with pytest.raises(ValidationError, match=pattern):
            TollVoucherCreateFactory.build({"origin": {field: invalid_value}})

    @pytest.mark.parametrize(
        "address, field",
        [
            pytest.param("origin", "zip_code", id="origin-zip-code"),
            pytest.param("origin", "state_acronym", id="origin-state-acronym"),
            pytest.param("origin", "country", id="origin-country"),
            pytest.param("destination", "number", id="destination-number"),
            pytest.param("destination", "point", id="destination-point"),
            pytest.param("destination", "country", id="destination-country"),
        ],
    )
    def test_without_optional_address_fields_success(
        self, session, address, field
    ):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build(
            params={address: {field: None}}
        )

        response = repository.create(toll_voucher_create)

        assert response.id is not None
        assert response.status is TollVoucherStatusTypes.DRAFT

    @pytest.mark.parametrize(
        "address, field",
        [
            pytest.param("origin", "city", id="origin-zip-code"),
            pytest.param("origin", "state", id="origin-state-acronym"),
            pytest.param("origin", "display_name", id="origin-country"),
            pytest.param("destination", "city", id="destination-number"),
            pytest.param("destination", "state", id="destination-point"),
            pytest.param(
                "destination", "display_name", id="destination-country"
            ),
        ],
    )
    def test_without_required_address_fields_error(self, address, field):
        with pytest.raises(ValidationError):
            TollVoucherCreateFactory.build(params={address: {field: None}})

    # Testes de veículo
    @pytest.mark.parametrize(
        "field, invalid_value, error_type",
        [
            pytest.param("plate", 5324542, "string_type", id="string-type-1"),
            pytest.param(
                "category", "Not a number", "int_parsing", id="string-type-2"
            ),
            pytest.param("toll_voucher_provider", 312231, "enum", id="enum-1"),
            pytest.param("toll_voucher_provider", True, "enum", id="enum-2"),
        ],
    )
    def test_with_invalid_vehicle_fields_error(
        self, field, invalid_value, error_type
    ):
        pattern = rf"\[type={error_type},.*\]"

        with pytest.raises(ValidationError, match=pattern):
            TollVoucherCreateFactory.build({"vehicle": {field: invalid_value}})

    @pytest.mark.parametrize("field", ["name"])
    def test_without_optional_vehicle_fields_success(self, session, field):
        repository = TollVoucherRepository(session)
        toll_voucher_create = TollVoucherCreateFactory.build(
            params={"vehicle": {field: None}}
        )

        response = repository.create(toll_voucher_create)

        assert response.id is not None
        assert response.status is TollVoucherStatusTypes.DRAFT

    @pytest.mark.parametrize(
        "field", ["plate", "category", "toll_voucher_provider"]
    )
    def test_without_required_vehicle_fields_error(self, field):
        with pytest.raises(ValidationError):
            TollVoucherCreateFactory.build(params={"vehicle": {field: None}})

    # Testes de embarcador

    @pytest.mark.parametrize(
        "field, invalid_value, error_type",
        [
            pytest.param("name", 5324542, "string_type", id="string-type-1"),
            pytest.param("name", 312.52, "string_type", id="string-type-2"),
            pytest.param(
                "document", 312231, "string_type", id="string-type-3"
            ),
        ],
    )
    def test_with_invalid_shipper_fields_error(
        self, field, invalid_value, error_type
    ):
        pattern = rf"\[type={error_type},.*\]"

        with pytest.raises(ValidationError, match=pattern):
            TollVoucherCreateFactory.build({"shipper": {field: invalid_value}})

    # ShipperCreate still doesn't have any optional fields,
    # therefore testing optional params would be irrelevant
    @pytest.mark.parametrize("field", ["name", "document"])
    def test_without_required_shipper_fields_error(self, field):
        with pytest.raises(ValidationError):
            TollVoucherCreateFactory.build(params={"shipper": {field: None}})
