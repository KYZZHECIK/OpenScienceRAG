from typing import Any
from src.open_science_rag.utils import get_secrets
from src.open_science_rag.query_filtering.queries import QueryType
from pyalex import Works, Authors, Institutions, config


Entity = Works | Authors | Institutions


class EntityClient:
    def __init__(self):
        self.mailto = get_secrets().open_alex_email

    @staticmethod
    def _choose_entity(entity: str) -> Entity:
        match (entity):
            case "authors": return Authors()
            case "works": return Works()
            case "institutions": return Institutions()
            case _: raise ValueError("Unknown entity")

    def build(self, q: QueryType) -> Entity:
        entity: Entity = EntityClient._choose_entity(q.entity)
        if self.mailto:
            config.email = self.mailto
        if q.search:
            entity = entity.search(q.search)
        if q.filter:
            entity = entity.filter(q.filter)
        if q.sort:
            entity = entity.sort(q.sort)
        if q.select:
            entity = entity.select(q.select)
        return entity

    def __call__(self, query: QueryType) -> list[dict[str, Any]]:
        return self.build(query).get()
