import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from requests import Request

from app.common.auth import Authorization
from main import get_app

"""
Note: Adiciona um middleware para a aplicação FastAPI que valida o Header
das requisições para garantir que o usuário está autenticado.
"""

app = get_app()


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    auth = Authorization()
    await auth(request)
    response = await call_next(request)
    return response


@app.get("/")
async def read_root():
    return {"Hello": "World"}


client = TestClient(app)


def test_authorization_success():
    response = client.get("/", headers={"Authorization": "Bearer test_token"})
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_authorization_failure_no_header():
    with pytest.raises(HTTPException):
        response = client.get("/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Usuário não autorizado"}
        assert response.headers["WWW-Authenticate"] == "Bearer"


def test_authorization_failure_wrong_scheme():
    with pytest.raises(HTTPException):
        response = client.get(
            "/", headers={"Authorization": "WrongBearer test_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {"detail": "Usuário não autorizado"}
        assert response.headers["WWW-Authenticate"] == "Bearer"
