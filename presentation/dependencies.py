from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from application import ConstructService
from persistence import ConstructDatastore
from persistence.db import get_db_session
from presentation.graphql.schema import GraphQLContext


def get_construct_datastore(
    session: AsyncSession = Depends(get_db_session),
) -> ConstructDatastore:
    return ConstructDatastore(session)


def get_construct_service(
    datastore: ConstructDatastore = Depends(get_construct_datastore),
) -> ConstructService:
    return ConstructService(datastore)


def get_graphql_context(
    service: ConstructService = Depends(get_construct_service),
) -> GraphQLContext:
    return GraphQLContext(construct_service=service)
