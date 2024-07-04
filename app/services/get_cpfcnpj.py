from app.infra.clients.minha_receita import MinhaReceitaClient
from app.schemas.get_cpfcnpj import (
    ErrorResponseSchema,
    SuccessResponseSchema,
)
from app.schemas.minhareceita import Empresa
from app.utils.formatters import format_cpf_cnpj


class GetCpfCnpj:
    """
    CarLicense - Uma classe construída para se
    comunicar com os serviços de consulta de placa.

    """

    def __init__(self) -> None:
        """
        Inicializa o CarLicense com instâncias de consulta de placa.
        """
        self.minha_receita = MinhaReceitaClient()

    async def get_cpf_cnpj(self, car_license: str):
        """
        Consulta a placa de um veículo para verificar se é
        elegível para compra de VPO ou não.

        :param car_license: A placa do veículo.
        :return: Todos os detalhes do veículo
        """
        result = {}

        formatted_cpfcnpj = format_cpf_cnpj(car_license)

        return_minha_receita = await self.minha_receita.get_cnpj(
            cnpj=formatted_cpfcnpj
        )

        try:
            result["data"] = [
                Empresa(**return_minha_receita),
            ]
            result["message"] = "Consulta realizada com sucesso."
            result["status_code"] = 200

            result = SuccessResponseSchema(**result)

        except Exception as error:
            result = ErrorResponseSchema(
                data=[], error=f"Erro ao consultar placa: {error}"
            )

        return result
