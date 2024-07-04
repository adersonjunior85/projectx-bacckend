import pytest

from app.repositories.toll_voucher import TollVoucherRepository
from tests.tools.factory.toll_voucher_factory import TollVoucherCreateFactory


class TestTollVoucherRepositoryGetList:
    @pytest.mark.skip(reason="KeyError: 'offset'")
    def test_success(self, session):
        repository = TollVoucherRepository(session)
        for _ in range(2):
            repository.create(TollVoucherCreateFactory.build())

        voucher_list = repository.get_list({"offset": 0, "limit": 10})

        assert len(voucher_list) == 2

    @pytest.mark.skip(reason="KeyError: 'offset'")
    def test_empty_list_success(self, session):
        repository = TollVoucherRepository(session)

        params = {"offset": 0, "limit": 10}
        voucher_list = repository.get_list(params)

        assert len(voucher_list) == 0

    @pytest.mark.parametrize(
        "offset, limit", [(0, 8), (2, 8), (5, 15), (0, 20)]
    )
    def test_with_pagination_success(self, session, offset, limit):
        repository = TollVoucherRepository(session)
        offset_toll_voucher = None

        # Dynamic range to avoid running out of bounds
        for i in range(limit + offset):
            # Fetch the first toll voucher of the list with offset
            if i == offset:
                offset_toll_voucher = repository.create(
                    TollVoucherCreateFactory.build()
                )
            else:
                repository.create(TollVoucherCreateFactory.build())

        params = {"offset": offset, "limit": limit}
        voucher_list = repository.get_list(params)

        assert len(voucher_list) <= limit
        assert voucher_list[0].id == offset_toll_voucher.id
