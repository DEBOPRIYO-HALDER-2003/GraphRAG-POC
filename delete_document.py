import json
from pathlib import Path

import faiss
import numpy as np
from config import VECTORSTORE_DIR
from services.ingestion_registry import IngestionRegistry
from llm.embeddings import EmbeddingService
from vectordb.faiss_store import FAISSStore
from graphdb.neo4j_store import Neo4jStore
from utils.logger import logger


class DocumentDeletionService:

    def __init__(self):

        self.registry = IngestionRegistry()

        self.embedding_service = EmbeddingService()

        self.vector_store = FAISSStore()

        self.neo4j = Neo4jStore()

        self.metadata_path = VECTORSTORE_DIR / "metadata.json"

        self.index_path = VECTORSTORE_DIR / "index.faiss"

    def load_metadata(self):

        if not self.metadata_path.exists():

            return []

        with open(self.metadata_path, "r", encoding="utf-8") as f:

            return json.load(f)

    def save_metadata(self, metadata):

        with open(self.metadata_path, "w", encoding="utf-8") as f:

            json.dump(
                metadata,
                f,
                indent=4,
                ensure_ascii=False,
            )

    def rebuild_faiss(self, metadata):

        if len(metadata) == 0:

            dimension = len(
                np.array(
                             self.embedding_service.embed_query("test"),
                             dtype=np.float32
                        )
                            )

            index = faiss.IndexFlatL2(dimension)

            faiss.write_index(
                index,
                str(self.index_path)
            )

            return

        texts = []

        for item in metadata:

            texts.append(item["text"])

        embeddings = self.embedding_service.embed_documents(texts)

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        dimension = embeddings.shape[1]

        index = faiss.IndexFlatL2(dimension)

        index.add(embeddings)

        faiss.write_index(
            index,
            str(self.index_path)
        )

    def remove_graph_entities(self, metadata):

        entity_names = set()

        for chunk in metadata:

            document = chunk.get("metadata", {})

            filename = document.get("filename")

            if filename is None:

                continue

        # Placeholder.
        # Entity ownership is not yet tracked,
        # so graph deletion cannot be performed accurately.
        # This will be improved after graph metadata is stored.

    def delete(self, filename):

        metadata = self.load_metadata()

        remaining = []

        removed = []

        for chunk in metadata:

            chunk_filename = chunk.get(
                "metadata",
                {}
            ).get(
                "filename"
            )

            if chunk_filename == filename:

                removed.append(chunk)

            else:

                remaining.append(chunk)

        if len(removed) == 0:

            logger.warning(
                "Document not found."
            )

            return

        logger.info(
            f"Removing {len(removed)} chunks."
        )

        self.save_metadata(
            remaining
        )

        logger.info(
            "Rebuilding FAISS..."
        )

        self.rebuild_faiss(
            remaining
        )

        logger.info(
            "Updating registry..."
        )

        self.registry.remove_document(
            filename
        )

        logger.info(
            "Removing graph data..."
        )

        self.remove_graph_entities(
            removed
        )

        self.neo4j.close()

        logger.info(
            "Deletion completed."
        )


def main():

    filename = input(
        "Enter filename to delete: "
    ).strip()

    service = DocumentDeletionService()

    service.delete(
        filename
    )


if __name__ == "__main__":

    main()