from fastapi import APIRouter
from strawberry.fastapi import GraphQLRouter

from presentation.dependencies import get_graphql_context
from presentation.graphql import schema


def create_router() -> APIRouter:
    router = APIRouter()
    graphql_router = GraphQLRouter(
        schema=schema,
        context_getter=get_graphql_context,
    )
    router.include_router(graphql_router, prefix="/graphql")

    @router.get("/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return router
