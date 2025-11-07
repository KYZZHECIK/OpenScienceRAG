from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from langchain_openai import ChatOpenAI
from src.open_science_rag.query_filtering.queries import QueryWrapper, QueryType
from src.open_science_rag.utils import get_secrets
from typing import Optional, Any


class QueryTranslator:
    template: str = """
                    You are an AI language model assistant. Your task is to translate the
                    user question into a structured response describing the query(s) that
                    will be translated into the necessary API call. 
                    User question: {question}
                    """

    def __init__(self, model_name: str = "gpt-4o-mini", temperature: float = 0, llm: Optional[Runnable[Any, Any]] = None) -> None:
        if llm is None:  # dependency injection for tests
            get_secrets()  # this will set OPENAI_API_KEY environment variable for self.llm
            llm = ChatOpenAI(model=model_name, temperature=temperature)
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=QueryWrapper)
        self.prompt = ChatPromptTemplate.from_template(
            QueryTranslator.template
        )

    def translate(self, user_question: str) -> QueryType:
        chain = self.prompt | self.llm | self.parser
        wrapper: QueryWrapper = chain.invoke({
            "question": user_question,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return wrapper.query
