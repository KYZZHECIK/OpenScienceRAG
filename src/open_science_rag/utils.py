import os
from dotenv import load_dotenv
from typing import NamedTuple


class SECRETS(NamedTuple):
    open_alex_email: str


def get_secrets() -> SECRETS:
    load_dotenv()
    return SECRETS(
        open_alex_email=os.environ["OPEN_ALEX_EMAIL"],
    )
