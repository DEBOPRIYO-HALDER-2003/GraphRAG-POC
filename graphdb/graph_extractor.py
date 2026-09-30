import json

from llm.chat import ChatService
from llm.prompts import GRAPH_EXTRACTION_PROMPT
from utils.logger import logger


class GraphExtractor:

    def __init__(self):

        self.chat = ChatService()

    def extract(self, text: str):

        prompt = GRAPH_EXTRACTION_PROMPT.format(
            text=text
        )

        response = self.chat.generate(prompt)

        try:

            data = json.loads(response)

            if "entities" not in data:
                data["entities"] = []

            if "relationships" not in data:
                data["relationships"] = []

            return data

        except Exception as e:

            logger.exception(e)

            logger.warning("Invalid JSON returned by LLM.")

            return {
                "entities": [],
                "relationships": []
            }