from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
from langchain_openai import ChatOpenAI
import src.open_science_rag.query_filtering.search_service as QFiltering
from src.open_science_rag.utils import get_secrets

parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
parser.add_argument('--user_question', type=str,
                    default="What is RAG?", help="User's question that will be used to gather context and answered")
parser.add_argument('--model_name', type=str,
                    default="gpt-4o-mini", help="Model name from OpenAI API")
parser.add_argument('--model_temperature', type=float,
                    default=0.0, help="Temperature for OpenAI model")


if __name__ == '__main__':
    args = parser.parse_args()
    get_secrets()
    llm = ChatOpenAI(model=args.model_name, temperature=args.model_temperature)

    service = QFiltering.SearchService(
        translator=QFiltering.QueryTranslator(llm=llm),
        entity_client=QFiltering.EntityClient()
    )

    results = service.search(args.user_question)
