import unittest
import json
from typing import Any
from langchain_core.runnables import RunnableLambda
from src.open_science_rag.query_filtering.queries import WorksQuery
from src.open_science_rag.query_filtering.translator import QueryTranslator


class FakeRunnable(RunnableLambda[Any, Any]):
    def __init__(self, response_payload: dict[str, Any]) -> None:
        self.response = json.dumps(response_payload)
        self.inputs: Any = []
        super().__init__(self._call)

    def _call(self, input: Any, config: Any = None):
        self.inputs.append(input)
        return self.response


class TestQueryTranslator(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        fake_llm = FakeRunnable(
            {
                "query": {
                    "entity": "works",
                    "search": "climate change"
                }
            }
        )
        self.translator = QueryTranslator(llm=fake_llm)

    def test_query_type_result(self):
        result = self.translator.translate(
            "I want to learn more about climate change, can you help me with that?")
        self.assertIsInstance(result, WorksQuery)
        self.assertEqual(result.entity, "works")
        self.assertEqual(result.search, "climate change")


if __name__ == '__main__':
    unittest.main()
