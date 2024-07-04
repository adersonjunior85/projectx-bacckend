from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("/liveness")
async def liveness():
    return {"application": True}


@health_router.get("/readiness")
async def readiness():
    try:
        # TODO Se aqui consegue alcançar todos os providers, readiness up
        pass
    except Exception:
        return {"provider": False}
