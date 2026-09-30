import uuid

from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import CHUNK_OVERLAP, CHUNK_SIZE
from models.chunk import Chunk


class Chunker:

    def __init__(self):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            separators=[
                "\n\n",
                "\n",
                ". ",
                "? ",
                "! ",
                ", ",
                " ",
                ""
            ]
        )

    def split(self, document):

        pieces = self.splitter.split_text(document.text)

        chunks = []

        for i, piece in enumerate(pieces):

            chunks.append(
                Chunk(
                    id=str(uuid.uuid4()),
                    document_id=document.id,
                    chunk_number=i + 1,
                    text=piece
                )
            )

        return chunks