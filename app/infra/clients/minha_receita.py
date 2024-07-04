import httpx

from config import settings


class MinhaReceitaClient:
    def __init__(self):
        self.URL = settings.MINHA_RECEITA_API

    async def get_cnpj(self, cnpj: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    url=f"{self.URL}/{cnpj}",
                    timeout=30,
                )
                response.raise_for_status()

            except Exception as error:
                return {
                    "provider": "MinhaReceita",
                    "detail": "Erro na requisição ao consultar "
                    f"cnpj no MinhaReceita: {error}",
                }

            response = response.json()

            return response
