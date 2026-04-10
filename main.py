from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from persistence.db import init_db
from presentation import create_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


def create_app(router: APIRouter) -> FastAPI:
    app = FastAPI(title="Simple GraphQL Service", lifespan=lifespan)
    app.include_router(router)
    return app


router = create_router()
app = create_app(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
