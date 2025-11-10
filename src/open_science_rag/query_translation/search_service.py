from src.open_science_rag.query_translation.translator import QueryTranslator
from src.open_science_rag.query_translation.entity_client import EntityClient


class SearchService:
    def __init__(self, translator: QueryTranslator, entity_client: EntityClient):
        self.translator = translator
        self.client = entity_client

    def search(self, user_question: str):
        query = self.translator.translate(user_question)
        return self.client(query)
