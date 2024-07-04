from typing import Tuple

from fastapi import HTTPException, Request, status


class Authorization:
    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization")
        scheme, credentials = self.get_authorization_scheme_param(
            authorization
        )
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuário não autorizado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        else:
            return authorization

    @staticmethod
    def get_authorization_scheme_param(
        authorization_header_value: str | None,
    ) -> Tuple[str, str]:
        if not authorization_header_value:
            return "", ""
        scheme, _, credentials = authorization_header_value.partition(" ")
        return scheme, credentials
