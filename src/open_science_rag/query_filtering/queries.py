from pydantic import BaseModel
from typing import Optional, Literal, Any


class Query(BaseModel):
    entity: Any = "base_query_entity"
    search: Optional[str] = None
    filter: Optional[dict[str, str]] = None

    # NOTE: Searching for keyword within filters (display name, title, fulltext, abstract, etc..)
    # TODO: Check PyAlex + OpenAlex docs to find the exact keys used, add them
    #       make the EntityClient build with adding .search_filter(filter="search value")
    search_filter: Optional[dict[str, str]] = None


class WorksQuery(Query):
    entity: Literal["works"] = "works"


class AuthorsQuery(Query):
    entity: str = "authors"


class InstitutionsQuery(Query):
    entity: str = "institutions"


QueryType = WorksQuery | AuthorsQuery | InstitutionsQuery


# Pydantic Output Parser from LangChain only accepts one base model,
# so we introduce this wrapper to just include all three
class QueryWrapper(BaseModel):
    query: QueryType
