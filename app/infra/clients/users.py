import httpx
from fastapi import Depends

from app.common.auth import Authorization
from app.exceptions.exceptions import BadRequest, RequestFailed
from app.utils.jwt import decode_jwt
from config import settings


class UsersClient:
    def __init__(self):
        self.URL = settings.URL_FMS_SESSIONS

    @staticmethod
    def _get_session_state(token: str):
        claims = decode_jwt(token=token)
        if claims.get("session_state", None):
            return claims["session_state"]
        return None

    async def get_user_by_token(
        self, token: str = Depends(Authorization())
    ) -> dict:
        """
        Consulta os dados do usuário a partir do token,
        que é decodificado e o session_state é extraído.
        A consulta é feita diretamente no FMS-SESSIONS.
        :param token: Token JWT
        :return: Dados do usuário
        """
        async with httpx.AsyncClient() as client:
            try:
                session_state = self._get_session_state(token=token)
                response = await client.get(
                    url=f"{self.URL}/sessions/{session_state}",
                    timeout=30,
                )
                response.raise_for_status()
            except Exception as error:
                raise RequestFailed(detail=str(error)) from error

            if response.status_code != 200:
                raise BadRequest(detail="Falha ao consultar dados do usuário.")

            return response.json()
