from domain import Construct, Sequence
from sqlalchemy import Select, select
from sqlalchemy.orm import Session, selectinload

from persistence.models import ConstructModel, SequenceModel


class ConstructDatastore:
    def __init__(self, session: Session) -> None:
        self._session = session

    def find_by_sequence(
        self,
        gene_name: str,
        min_length: int | None = None,
    ) -> list[Construct]:
        """Return constructs with at least one sequence matching the filters."""
        stmt: Select[tuple[ConstructModel]] = (
            select(ConstructModel)
            .options(selectinload(ConstructModel.sequences))
            .join(ConstructModel.sequences)
            .where(SequenceModel.gene_name == gene_name)
        )

        if min_length is not None:
            stmt = stmt.where(SequenceModel.length >= min_length)

        stmt = stmt.distinct().order_by(ConstructModel.id)
        return [self._to_domain(model) for model in self._session.scalars(stmt)]

    @staticmethod
    def _to_domain(model: ConstructModel) -> Construct:
        return Construct(
            id=model.id,
            name=model.name,
            sequences=tuple(
                Sequence(
                    id=sequence.id,
                    gene_name=sequence.gene_name,
                    length=sequence.length,
                )
                for sequence in model.sequences
            ),
        )
