from typing import Union

from aiservice.main.utils import AILog
from src.aiservice.main.entity import Expense
from src.aiservice.main.utils import MessageParser
from src.aiservice.main.service import LLMService


class MessageService:
    def __init__(self):
        self._parser = MessageParser()
        self._llmservice = LLMService()
        self.messageLog = AILog(name="MessageService")

    def process(self, message: str) -> Union[None, Expense]:
        if not self._parser.parse_message(message):
            self.messageLog.error("Invalid Message")
            return None
        try:
            return self._llmservice.run(message)
        except Exception as e:
            self.messageLog.error(f"Error: {str(e)}")
            raise e