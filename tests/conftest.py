from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from config import settings
from main import get_app

if settings.current_env in [
    "development",
    "homologation",
    "staging",
    "production",
]:
    raise Exception(
        "Não é permitido executar os testes "
        f"no ambiente: {settings.current_env}. "
        "Por favor, execute o comando 'export API_ENV=testing'"
    )


@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture()
def client(session: Session):
    def get_session_override():
        return session

    app = get_app()

    # app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    # app.dependency_overrides.clear()


@pytest.fixture(scope="session")
def token_jwt() -> str:
    access_token = (
        "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJRZVZ3QTRwMHJCRTNJ"
        "Y3p2ZXJDZ2tvLWNDTFUzNlBUaEtVME11cmNYeDNZIn0.eyJqdGkiOiI1OGQ0NzFhZC0y"
        "MTEzLTRmYjEtYjNkZS04Yjk3YjZhMjc3MzkiLCJleHAiOjE3MjE3NjU4OTQsIm5iZiI6"
        "MCwiaWF0IjoxNzEzOTg5ODk0LCJpc3MiOiJodHRwOi8va2V5Y2xvYWstaHR0cC9hdXRo"
        "L3JlYWxtcy9zaGlwcGVyIiwic3ViIjoiMmJhMzk4MTAtODU2OC00NGY0LWI5MTUtMDI3"
        "MzIxMjQ4MzFhIiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiYXBpIiwiYXV0aF90aW1lIjow"
        "LCJzZXNzaW9uX3N0YXRlIjoiYzUyNzEwZTItZjc2NS00ZDI4LTg2YWQtN2M5MWI0ZjNh"
        "MjU4IiwiYWNyIjoiMSIsInNjb3BlIjoiIiwib2ZmaWNlcyI6WyI4MmZkY2Y4Mi04Mzkx"
        "LTRkZTktOGEwZS0xYjViYWQ5MzYzZGEiLCJiZmYwMjM3YS0yYTMzLTQyM2UtOGUzMS0y"
        "YTQ5YWFkZDc5ZTEiLCI3YzcyMjRhYS04ZmFjLTQyZDUtYTY3OC1kNjBkODkwODY3ZmMi"
        "XSwidXNlciI6eyJpZCI6ImEwMDJlNjc3LWU3NDMtNGY3Yy1hNjExLTlhM2Y5ZjI4NTM2"
        "YyJ9fQ.fxyrCzBFPG2o7YR0qWChkZplJq5QWaTqP6wh43-jy4u94GTZluIviCNLOFdDA"
        "2w62WhF1_JmezRfzDgLWziLoAoH1d0UGQ41bG4HtFzGW2XM19yCoAN9nJCc42dXPYr9U"
        "CdiZLjHICBfp3BB4wzEY4ya0UNUbeVaxj60kGvyUXeStqSuezYzTI4JQyA9RAThoVUkj"
        "OP6sDFMCsuqREwYtcVomm5ByYMvADdNW_uRYVA-rFqV6AzXMtbSD3gryy-tYi4uVZxr8"
        "VMnHseoDyS1q7CMAdCi1PceasPTHgSAq7atVuR9h65qo0LIBUqKqKfdtQMXPR6u6E7Mq"
        "P8KLy_oEw"
    )
    return access_token


@pytest.fixture(scope="session")
def headers(token_jwt) -> dict[str, Any]:
    return {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_jwt}",
    }
