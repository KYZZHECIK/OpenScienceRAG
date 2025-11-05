from pydantic import BaseModel
from typing import Optional, Literal, Any, Union


class Query(BaseModel):
    entity: Any = "base_query_entity"
    search: Optional[str] = None
    filter: Optional[str] = None
    sort: Optional[str] = None
    per_page: int = 20
    select: Optional[str] = None


class WorksQuery(Query):
    entity: Literal["works"] = "works"
    select: Optional[str] = (
        "id,display_name,publication_year,abstract_inverted_index,authorships"
    )


class AuthorsQuery(Query):
    entity: str = "authors"
    select: Optional[str] = (
        "id,display_name,works_count,affiliations"
    )


class InstitutionsQuery(Query):
    entity: str = "institutions"
    select: Optional[str] = (
        "id,display_name,works_count,ror"
    )


QueryType = WorksQuery | AuthorsQuery | InstitutionsQuery


class QueryWrapper(BaseModel):
    query: QueryType
