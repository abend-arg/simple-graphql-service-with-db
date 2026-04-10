import asyncio

from sqlalchemy import select

from persistence.db import SessionLocal
from persistence.models import ConstructModel, SequenceModel


async def seed() -> None:
    async with SessionLocal() as session:
        existing_names = set((await session.scalars(select(ConstructModel.name))).all())
        constructs = [
            ConstructModel(
                name="BRCA1 Panel",
                sequences=[
                    SequenceModel(gene_name="BRCA1", length=1863),
                    SequenceModel(gene_name="BRCA1", length=923),
                ],
            ),
            ConstructModel(
                name="TP53 Screening",
                sequences=[
                    SequenceModel(gene_name="TP53", length=1179),
                    SequenceModel(gene_name="TP53", length=642),
                ],
            ),
            ConstructModel(
                name="EGFR Validation",
                sequences=[
                    SequenceModel(gene_name="EGFR", length=1210),
                ],
            ),
        ]

        records_to_insert = [
            construct for construct in constructs if construct.name not in existing_names
        ]
        if not records_to_insert:
            return

        session.add_all(records_to_insert)
        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
