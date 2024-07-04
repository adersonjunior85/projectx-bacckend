import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import PlainTextResponse

from app import vpo_ascii
from app.models.entities import *  # noqa: import all models on startup
from app.routers.v1 import router
from config import settings

logger = logging.getLogger(__name__)


def get_app() -> FastAPI:
    app = FastAPI(
        root_path=settings.ROOT_PATH,
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
    )

    app.add_middleware(
        middleware_class=CORSMiddleware,  # noqa https://github.com/tiangolo/fastapi/discussions/10968
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router=router)

    @app.get("")
    def index():
        return PlainTextResponse(vpo_ascii)

    @app.get("/favicon.ico")
    def root():
        return {"message": "project-x-api is up and running"}

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:get_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        log_level=settings.LOG_LEVEL.lower(),
        factory=True,
    )
