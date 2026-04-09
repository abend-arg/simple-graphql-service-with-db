from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from persistence.models import ConstructModel, SequenceModel


class ConstructDatastore:
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[ConstructModel]:
        """Return constructs with at least one sequence matching the filters."""
        stmt: Select[tuple[ConstructModel]] = (
            select(ConstructModel)
            .join(ConstructModel.sequences)
            .where(SequenceModel.gene_name == gene_name)
        )

        if min_length is not None:
            stmt = stmt.where(SequenceModel.length >= min_length)

        stmt = stmt.distinct().order_by(ConstructModel.id)
        return list(self._session.scalars(stmt))

