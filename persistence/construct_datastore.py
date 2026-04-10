from domain import Construct, ConstructSequenceFilter, Sequence
from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from persistence.models import ConstructModel, SequenceModel


class ConstructDatastore:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_sequence(self, filters: ConstructSequenceFilter) -> list[Construct]:
        """Return constructs with at least one sequence matching the filters."""
        stmt: Select[tuple[ConstructModel]] = (
            select(ConstructModel)
            .options(selectinload(ConstructModel.sequences))
            .join(ConstructModel.sequences)
            .where(SequenceModel.gene_name == filters.gene_name)
        )

        if filters.min_length is not None:
            stmt = stmt.where(SequenceModel.length >= filters.min_length)

        stmt = stmt.distinct().order_by(ConstructModel.id)
        result = await self._session.scalars(stmt)
        return [self._to_domain(model) for model in result]

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
