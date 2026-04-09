from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from strawberry.fastapi import GraphQLRouter

from persistence.db import init_db
from presentation.dependencies import get_graphql_context
from presentation.graphql import schema


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    init_db()
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Simple GraphQL Service", lifespan=lifespan)

    graphql_router = GraphQLRouter(
        schema=schema,
        context_getter=get_graphql_context,
    )
    app.include_router(graphql_router, prefix="/graphql")

    @app.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
