import json
import faiss
import numpy as np

from config import VECTORSTORE_DIR
from utils.logger import logger


class FAISSStore:

    def __init__(self):

        VECTORSTORE_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        self.index_path = VECTORSTORE_DIR / "index.faiss"
        self.metadata_path = VECTORSTORE_DIR / "metadata.json"

        self.dimension = 768

        if self.index_path.exists():

            self.index = faiss.read_index(
                str(self.index_path)
            )

        else:

            self.index = faiss.IndexFlatL2(
                self.dimension
            )

        if self.metadata_path.exists():

            with open(
                self.metadata_path,
                "r",
                encoding="utf-8"
            ) as f:

                self.metadata = json.load(f)

        else:

            self.metadata = []

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------

    def save(self):

        faiss.write_index(
            self.index,
            str(self.index_path)
        )

        with open(
            self.metadata_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ---------------------------------------------------------
    # ADD CHUNKS
    # ---------------------------------------------------------

    def add_chunks(self, chunks):

        embeddings = []

        # IDs already stored in FAISS metadata
        existing_ids = {
            item["chunk_id"]
            for item in self.metadata
        }

        # Texts already stored
        existing_texts = {
            item["text"].strip()
            for item in self.metadata
        }

        new_chunks = []

        for chunk in chunks:

            chunk_id = chunk.id
            chunk_text = chunk.text.strip()

            # ---------------------------------------------
            # Skip duplicate chunk ID
            # ---------------------------------------------

            if chunk_id in existing_ids:

                logger.info(
                    f"Skipping duplicate chunk ID: {chunk_id}"
                )

                continue

            # ---------------------------------------------
            # Skip identical chunk text
            # ---------------------------------------------

            if chunk_text in existing_texts:

                logger.info(
                    "Skipping duplicate chunk text."
                )

                continue

            new_chunks.append(chunk)

            embeddings.append(
                chunk.embedding
            )

            self.metadata.append(
                {
                    "chunk_id": chunk_id,
                    "document_id": chunk.document_id,
                    "chunk_number": chunk.chunk_number,
                    "text": chunk.text,
                    "metadata": chunk.metadata
                }
            )

            existing_ids.add(chunk_id)
            existing_texts.add(chunk_text)

        # ---------------------------------------------
        # Nothing new
        # ---------------------------------------------

        if not new_chunks:

            logger.info(
                "No new chunks to add."
            )

            return

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        # ---------------------------------------------
        # Add embeddings to FAISS
        # ---------------------------------------------

        self.index.add(
            embeddings
        )

        self.save()

        logger.info(
            f"Added {len(new_chunks)} new chunk(s) to FAISS."
        )

    # ---------------------------------------------------------
    # SEARCH
    # ---------------------------------------------------------

    def search(
        self,
        embedding,
        k=5
    ):

        # No documents in FAISS
        if self.index.ntotal == 0:

            logger.warning(
                "FAISS index is empty."
            )

            return []

        # Never request more results than available
        k = min(
            k,
            self.index.ntotal
        )

        query_vector = np.array(
            [embedding],
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_vector,
            k
        )

        results = []

        seen_ids = set()
        seen_texts = set()

        for index in indices[0]:

            # FAISS can return -1 when no valid result exists
            if index < 0:
                continue

            # Protect against metadata mismatch
            if index >= len(self.metadata):
                continue

            chunk = self.metadata[index]

            chunk_id = chunk["chunk_id"]
            chunk_text = chunk["text"].strip()

            # ---------------------------------------------
            # Remove duplicate chunk IDs
            # ---------------------------------------------

            if chunk_id in seen_ids:
                continue

            # ---------------------------------------------
            # Remove identical text
            # ---------------------------------------------

            if chunk_text in seen_texts:
                continue

            seen_ids.add(chunk_id)
            seen_texts.add(chunk_text)

            results.append(chunk)

        return results
    