from pathlib import Path
from typing import List

from config import UPLOAD_DIR
from loaders.document_loader import DocumentLoader
from processing.cleaner import TextCleaner
from processing.metadata import MetadataGenerator
from processing.chunker import Chunker
from llm.embeddings import EmbeddingService
from vectordb.faiss_store import FAISSStore
from services.ingestion_registry import IngestionRegistry
from utils.hash_utils import calculate_file_hash
from utils.logger import logger
from graphdb.graph_extractor import GraphExtractor
from graphdb.neo4j_store import Neo4jStore


class IngestionPipeline:

    def __init__(self):

        self.loader = DocumentLoader()

        self.chunker = Chunker()

        self.embedding_service = EmbeddingService()

        self.vector_store = FAISSStore()
        
        self.graph_extractor = GraphExtractor()

        self.neo4j = Neo4jStore()

        self.registry = IngestionRegistry()

    def get_documents(self) -> List[Path]:

        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        files = []

        for file in UPLOAD_DIR.iterdir():

            if file.is_file():

                if file.suffix.lower() in [
                    ".pdf",
                    ".docx",
                    ".pptx",
                    ".txt",
                    ".csv",
                    ".xlsx",
                ]:
                    files.append(file)

        return sorted(files)

    def process_document(self, file_path: Path):

        logger.info("=" * 80)

        logger.info(f"Processing : {file_path.name}")

        file_hash = calculate_file_hash(str(file_path))

        if self.registry.is_ingested(file_path.name, file_hash):

            logger.info("Already ingested. Skipping.")

            return

        logger.info("Loading document...")

        document = self.loader.load(str(file_path))

        logger.info("Cleaning text...")

        document.text = TextCleaner.clean(document.text)

        logger.info("Generating metadata...")

        document = MetadataGenerator.generate(document)

        logger.info("Chunking document...")

        chunks = self.chunker.split(document)

        logger.info(f"Total Chunks : {len(chunks)}")

        if len(chunks) == 0:

            logger.warning("No chunks generated.")

            return

        logger.info("Generating embeddings...")

        texts = []

        for chunk in chunks:

            chunk.metadata = document.metadata.copy()

            chunk.metadata["filename"] = document.filename

            chunk.metadata["document_id"] = document.id

            texts.append(chunk.text)

        embeddings = self.embedding_service.embed_documents(texts)

        for chunk, embedding in zip(chunks, embeddings):

            chunk.embedding = embedding

        logger.info("Saving vectors to FAISS...")

        self.vector_store.add_chunks(chunks)

        logger.info("Building Graph...")

        for chunk in chunks:

            extraction = self.graph_extractor.extract(
                chunk.text
            )

            self.neo4j.save_extraction(
                document_id=document.id,
                filename=document.filename,
                chunk_id=chunk.id,
                chunk_text=chunk.text,
                chunk_index=chunk.chunk_number,
                extraction=extraction,
            )
        logger.info("Updating registry...")

        self.registry.add_document(
            file_path.name,
            file_hash
        )

        logger.info("Completed.")

    def run(self):

        files = self.get_documents()

        if len(files) == 0:

            logger.warning("No documents found.")

            return

        logger.info(f"Found {len(files)} document(s).")

        for file in files:

            try:

                self.process_document(file)

            except Exception as e:

                logger.exception(e)
                
        self.neo4j.close()
        logger.info("=" * 80)
        logger.info("INGESTION FINISHED")
        logger.info("=" * 80)

        logger.info(f"Processed Documents : {len(files)}")


def main():

    pipeline = IngestionPipeline()

    pipeline.run()


if __name__ == "__main__":

    main()