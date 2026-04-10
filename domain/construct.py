from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Sequence:
    id: int
    gene_name: str
    length: int


@dataclass(frozen=True)
class Construct:
    id: int
    name: str
    sequences: tuple[Sequence, ...]
