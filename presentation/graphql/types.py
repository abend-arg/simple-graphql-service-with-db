from __future__ import annotations

import strawberry

from domain import Construct as ConstructDTO
from domain import Sequence as SequenceDTO


@strawberry.type
class Sequence:
    id: int
    gene_name: str
    length: int

    @classmethod
    def from_domain(cls, model: SequenceDTO) -> "Sequence":
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
    def from_domain(cls, model: ConstructDTO) -> "Construct":
        return cls(
            id=model.id,
            name=model.name,
            sequences=[Sequence.from_domain(sequence) for sequence in model.sequences],
        )
