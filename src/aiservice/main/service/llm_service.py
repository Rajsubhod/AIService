import os
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

from src.aiservice.main.entity import Expense


class LLMService:
    def __init__(self):
        load_dotenv()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are an expert extraction algorithm. "
                    "Only extract relevant information from the text. "
                    "If you do not know the value of an attribute asked to extract, "
                    "return null for the attribute's value.",
                ),
                ("human", "{text}")
            ]
        )
        self.api_key = os.getenv("LLM_KEY")
        self.llm = ChatMistralAI(api_key=self.api_key, model="mistral-large-2402",max_retries=3)
        self.runnable = self.prompt | self.llm.with_structured_output(schema=Expense)

    def run(self,message :str)-> dict | Expense:
        try:
            return self.runnable.invoke({"text": message})
        except Exception as e:
            raise e