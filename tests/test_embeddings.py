import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from llm.embeddings import EmbeddingService


def main():

    embedding_service = EmbeddingService()

    text = """
    Artificial Intelligence is transforming industries
    through machine learning and large language models.
    """

    print("=" * 80)

    print("Generating embedding...")

    vector = embedding_service.embed_text(text)

    print()

    print("Embedding dimension :", len(vector))

    print()

    print("First 10 values:")

    print(vector[:10])


if __name__ == "__main__":
    main()