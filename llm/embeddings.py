from typing import List

from langchain_ollama import OllamaEmbeddings

from config import EMBED_MODEL


class EmbeddingService:
    """
    Wrapper around Ollama embedding model.
    """

    def __init__(self):

        self.model = OllamaEmbeddings(
            model=EMBED_MODEL
        )

    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        """

        return self.model.embed_query(text)

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        """

        return self.model.embed_documents(texts)