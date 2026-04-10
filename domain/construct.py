from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sequence:
    id: int
    gene_name: str
    length: int


@dataclass(frozen=True)
class ConstructSequenceFilter:
    gene_name: str
    min_length: int | None = None


@dataclass(frozen=True)
class Construct:
    id: int
    name: str
    sequences: tuple[Sequence, ...]
