from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_openai import ChatOpenAI
from src.open_science_rag.query_filtering.queries import QueryWrapper, QueryType


class QueryTranslator:
    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0) -> None:
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.parser = PydanticOutputParser(pydantic_object=QueryWrapper)
        self.prompt = ChatPromptTemplate.from_messages(["#TODO"])

    def translate(self, user_query: str) -> QueryType:
        chain = self.prompt | self.llm | self.parser
        return chain.invoke({
            "user_query": user_query,
            "format_instructions": self.parser.get_format_instructions(),
        })
