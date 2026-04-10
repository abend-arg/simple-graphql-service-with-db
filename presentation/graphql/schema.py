import strawberry
from strawberry.fastapi import BaseContext
from strawberry.types import Info

from application import ConstructService
from domain import ConstructSequenceFilter
from presentation.graphql.types import Construct


class GraphQLContext(BaseContext):
    def __init__(self, construct_service: ConstructService) -> None:
        super().__init__()
        self.construct_service = construct_service


@strawberry.input
class ConstructSequenceFilterInput:
    gene_name: str
    min_length: int | None = None

    def to_domain(self) -> ConstructSequenceFilter:
        return ConstructSequenceFilter(
            gene_name=self.gene_name,
            min_length=self.min_length,
        )


@strawberry.type
class Query:
    @strawberry.field
    async def constructs_by_sequence(
        self,
        info: Info[GraphQLContext, None],
        filters: ConstructSequenceFilterInput,
    ) -> list[Construct]:
        constructs = await info.context.construct_service.list_constructs_by_sequence(
            filters=filters.to_domain(),
        )
        return [Construct.from_domain(construct) for construct in constructs]


schema = strawberry.Schema(query=Query)
