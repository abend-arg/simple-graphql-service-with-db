from __future__ import annotations

import strawberry

from persistence.models import ConstructModel, SequenceModel


@strawberry.type
class Sequence:
    id: int
    gene_name: str
    length: int

    @classmethod
    def from_model(cls, model: SequenceModel) -> "Sequence":
        return cls(
            id=model.id,
            gene_name=model.gene_name,
            length=model.length,
        )


@strawberry.type
class Construct:
    id: int
    name: str
    sequences: list[Sequence]

    @classmethod
    def from_model(cls, model: ConstructModel) -> "Construct":
        return cls(
            id=model.id,
            name=model.name,
            sequences=[Sequence.from_model(sequence) for sequence in model.sequences],
        )

