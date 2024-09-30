from typing import Union
from src.aiservice.main.entity import Expense
from src.aiservice.main.utils import MessageParser
from src.aiservice.main.service import LLMService


class MessageService:
    def __init__(self):
        self._parser = MessageParser()
        self._llmservice = LLMService()

    def process(self, message: str) -> Union[None, Expense]:
        if not self._parser.parse_message(message):
            return None
        try:
            return self._llmservice.run(message)
        except Exception as e:
            raise e