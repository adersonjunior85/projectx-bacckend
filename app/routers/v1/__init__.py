from fastapi.routing import APIRouter

from app.routers.v1.get_cpfcnpj import getcpfcnpj_route
from app.routers.v1.health_check import health_router

router = APIRouter(prefix="/v1", redirect_slashes=True)

router.include_router(
    router=health_router,
    prefix="/health",
    tags=["Health"],
)

router.include_router(
    router=getcpfcnpj_route,
    prefix="/cpfcnpj",
    tags=["Cpf e Cnpj"],
)
