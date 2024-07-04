from fastapi import APIRouter, Depends, status
from fastapi.security import HTTPBearer

# from app.common.auth import AuthUser
from app.services.get_cpfcnpj import GetCpfCnpj

getcpfcnpj_route = APIRouter(
    # dependencies=[Depends(HTTPBearer(auto_error=False))]
)


@getcpfcnpj_route.get(
    "/{cnpj}",
    description="Consulta de placas de veículos nos provedores",
    status_code=status.HTTP_200_OK,
)
async def get_cpfcnpj(
    cnpj: str,
    # user: dict = Depends(AuthUser.get_user_data),
):
    """
    Endpoint para consulta de cpf.

    Sumario

    :param cnpj: Cnpj a ser consultado.
    :return: Dados do cnpj, se encontrado.
    """

    service = GetCpfCnpj()
    result = await service.get_cpf_cnpj(cnpj)
    return result
