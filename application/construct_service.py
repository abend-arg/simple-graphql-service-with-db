from typing import Protocol

from domain import Construct, ConstructSequenceFilter


class ConstructDatastorePort(Protocol):
    async def find_by_sequence(self, filters: ConstructSequenceFilter) -> list[Construct]:
        ...


class ConstructService:
    def __init__(self, datastore: ConstructDatastorePort) -> None:
        self._datastore = datastore

    async def list_constructs_by_sequence(
        self,
        filters: ConstructSequenceFilter,
    ) -> list[Construct]:
        return await self._datastore.find_by_sequence(filters)
