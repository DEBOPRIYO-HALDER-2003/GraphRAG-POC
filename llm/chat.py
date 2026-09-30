from langchain_ollama import ChatOllama

from config import CHAT_MODEL


class ChatService:
    """
    Wrapper around Ollama chat model.
    """

    def __init__(self):

        self.llm = ChatOllama(
            model=CHAT_MODEL,
            temperature=0
        )

    def generate(self, prompt: str) -> str:
        """
        Generate response from LLM.
        """

        response = self.llm.invoke(prompt)

        return response.content