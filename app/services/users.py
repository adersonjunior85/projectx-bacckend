import json

from app.exceptions.exceptions import BadRequest, UnauthorizedError
from app.infra.clients.users import UsersClient


class UsersService:
    def __init__(self):
        self.client = UsersClient()

    async def get_user_data(self) -> dict:
        user = await self.client.get_user_by_token()
        user = json.loads(user["session_data"])
        if not user:
            raise BadRequest(detail="Usuário não encontrado.")

        status = user.get("status", None)
        if status != "approved":
            raise UnauthorizedError(
                detail="Usuário não encontra-se com o status aprovado."
            )

        offices = user.get("offices", [])
        if not offices:
            raise UnauthorizedError(
                detail="Usuário não possui nenhum vinculo com empresas."
            )

        return user
