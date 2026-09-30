import sys
import uuid
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from llm.embeddings import EmbeddingService
from models.chunk import Chunk
from vectordb.faiss_store import FAISSStore


def main():

    embedding_service = EmbeddingService()

    store = FAISSStore()

    texts = [

        "Artificial Intelligence is transforming healthcare.",

        "Neo4j is a graph database.",

        "FAISS performs vector similarity search.",

        "LangChain helps build LLM applications.",

        "Ollama runs local language models."

    ]

    chunks = []

    print("=" * 80)
    print("Generating embeddings...")

    for i, text in enumerate(texts):

        chunk = Chunk(

            id=str(uuid.uuid4()),

            document_id="demo",

            chunk_number=i + 1,

            text=text,

            embedding=embedding_service.embed_text(text)
        )

        chunks.append(chunk)

    print("Adding vectors to FAISS...")

    store.add_chunks(chunks)

    print()

    question = "Which database stores graphs?"

    print("Query :", question)

    query_embedding = embedding_service.embed_text(question)

    results = store.search(query_embedding, top_k=3)

    print()

    print("=" * 80)

    print("Top Results\n")

    for result in results:

        print(f"Score : {result['score']:.4f}")

        print(result["text"])

        print("-" * 60)


if __name__ == "__main__":
    main()