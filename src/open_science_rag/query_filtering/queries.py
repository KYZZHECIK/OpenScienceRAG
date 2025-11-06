from pydantic import BaseModel
from typing import Optional, Literal, Any


class Query(BaseModel):
    entity: Any = "base_query_entity"
    search: Optional[str] = None
    filter: Optional[dict[str, str]] = None
    sort: Optional[str] = None

    # FIXME: per_page is only used in .paginate(),
    # if we do plain .get() we get the first page by default 25 entries
    per_page: int = 20
    # FIXME: Redo the select https://docs.openalex.org/how-to-use-the-api/get-lists-of-entities/select-fields
    # Also, it is a list of str in PyAlex.
    select: Optional[str] = None


class WorksQuery(Query):
    entity: Literal["works"] = "works"
    select: Optional[str] = (
        ""
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


# Pydantic Output Parser from LangChain only accepts one base model,
# so we introduce this wrapper to just include all three
class QueryWrapper(BaseModel):
    query: QueryType
