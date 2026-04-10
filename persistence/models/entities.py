from __future__ import annotations

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from persistence.models.base import Base


class ConstructModel(Base):
    __tablename__ = "constructs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    sequences: Mapped[list[SequenceModel]] = relationship(
        back_populates="construct",
        cascade="all, delete-orphan",
    )


class SequenceModel(Base):
    __tablename__ = "sequences"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    gene_name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    length: Mapped[int] = mapped_column(Integer, nullable=False)
    construct_id: Mapped[int] = mapped_column(
        ForeignKey("constructs.id", ondelete="CASCADE"),
        nullable=False,
    )

    construct: Mapped[ConstructModel] = relationship(back_populates="sequences")
