from typing import Protocol

from persistence.models import ConstructModel


class ConstructDatastorePort(Protocol):
    def find_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[ConstructModel]:
        ...


class ConstructService:
    def __init__(self, datastore: ConstructDatastorePort) -> None:
        self._datastore = datastore

    def list_constructs_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[ConstructModel]:
        return self._datastore.find_by_sequence(
            gene_name=gene_name,
            min_length=min_length,
        )

