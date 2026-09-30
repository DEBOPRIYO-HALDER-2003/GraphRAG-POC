from llm.embeddings import EmbeddingService
from vectordb.faiss_store import FAISSStore


class Retriever:

    def __init__(self):

        self.embedding_service = EmbeddingService()

        self.vector_store = FAISSStore()

    def retrieve(
        self,
        question: str,
        top_k: int = 5
    ):

        query_embedding = self.embedding_service.embed_text(
            question
        )

        results = self.vector_store.search(
            embedding=query_embedding,
            k=top_k
        )

        # Remove duplicate chunks
        unique_results = []

        seen_ids = set()
        seen_texts = set()

        for chunk in results:

            chunk_id = chunk["chunk_id"]
            chunk_text = chunk["text"].strip()

            # Skip duplicate ID
            if chunk_id in seen_ids:
                continue

            # Skip identical text
            if chunk_text in seen_texts:
                continue

            seen_ids.add(chunk_id)
            seen_texts.add(chunk_text)

            unique_results.append(chunk)

        return unique_results