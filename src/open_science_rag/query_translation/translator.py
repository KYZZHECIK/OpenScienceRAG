from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.runnables import Runnable
from src.open_science_rag.query_translation.queries import QueryWrapper, QueryType
from typing import Any, TypeAlias, cast

# We keep it as general as possible for easier test injections
LLM: TypeAlias = Runnable[Any, Any]


class QueryTranslator:
    template: str = """
                    You are an AI language model assistant. Your task is to translate the
                    user question into a structured response describing the query(s) that
                    will be translated into the necessary API call. 

                    User question: {question}

                    You MUST follow these formatting instructions EXACTLY:
                    {format_instructions}
                    """

    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        self.parser = PydanticOutputParser(pydantic_object=QueryWrapper)
        self.prompt = ChatPromptTemplate.from_template(
            QueryTranslator.template
        )

    def translate(self, user_question: str) -> QueryType:
        chain = cast(
            Runnable[dict[str, str], QueryWrapper],
            self.prompt | self.llm | self.parser,
        )
        wrapper: QueryWrapper = chain.invoke({
            "question": user_question,
            "format_instructions": self.parser.get_format_instructions(),
        })
        return wrapper.query
