import src.open_science_rag.query_filtering.search_service as QFiltering


if __name__ == '__main__':
    service = QFiltering.SearchService(
        translator=QFiltering.QueryTranslator(),
        entity_client=QFiltering.EntityClient()
    )

    results = service.search("Who asked?")
