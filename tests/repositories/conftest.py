import pytest

from app.repositories.toll_voucher import TollVoucherRepository


@pytest.fixture(scope="class")
def create_toll_voucher(mocker):
    return mocker.Mock(spec=TollVoucherRepository)
