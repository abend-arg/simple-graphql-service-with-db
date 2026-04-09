import strawberry
from strawberry.fastapi import BaseContext
from strawberry.types import Info

from application import ConstructService
from presentation.graphql.types import Construct


class GraphQLContext(BaseContext):
    def __init__(self, construct_service: ConstructService) -> None:
        self.construct_service = construct_service


@strawberry.type
class Query:
    @strawberry.field
    def constructs_by_sequence(
        self,
        info: Info[GraphQLContext, None],
        gene_name: str,
        min_length: int | None = None,
    ) -> list[Construct]:
        models = info.context.construct_service.list_constructs_by_sequence(
            gene_name=gene_name,
            min_length=min_length,
        )
        return [Construct.from_model(model) for model in models]


schema = strawberry.Schema(query=Query)
