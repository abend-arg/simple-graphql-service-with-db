from typing import Protocol

from domain import Construct


class ConstructDatastorePort(Protocol):
    async def find_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[Construct]:
        ...


class ConstructService:
    def __init__(self, datastore: ConstructDatastorePort) -> None:
        self._datastore = datastore

    async def list_constructs_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[Construct]:
        return await self._datastore.find_by_sequence(
            gene_name=gene_name,
            min_length=min_length,
        )
