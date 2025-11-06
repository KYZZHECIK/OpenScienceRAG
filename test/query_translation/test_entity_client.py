import unittest
from src.open_science_rag.query_filtering.entity_client import EntityClient
from src.open_science_rag.query_filtering.queries import WorksQuery, InstitutionsQuery


class TestEntityClient(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.client = EntityClient()

    def test_institution_search(self):
        query = InstitutionsQuery(
            search="Charles University",
            select=None  # FIXME: Temporary until we figure out what select is
        )
        result = self.client(query)

        # id is OpenAlex ID, which contains the domain
        result_cu_id = result[0]["id"]
        expected_cu_id = "https://openalex.org/I21250087"
        self.assertEqual(result_cu_id, expected_cu_id)

    def test_work_search(self):
        # TODO


if __name__ == '__main__':
    unittest.main(verbosity=2)
