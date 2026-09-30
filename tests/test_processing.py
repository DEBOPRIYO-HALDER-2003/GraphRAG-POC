import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from loaders.document_loader import DocumentLoader
from processing.cleaner import TextCleaner
from processing.metadata import MetadataGenerator
from processing.chunker import Chunker

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"


def main():

    files = list(UPLOAD_DIR.iterdir())

    if not files:
        print("No files found.")
        return

    loader = DocumentLoader()
    chunker = Chunker()

    for file in files:

        print("=" * 80)

        document = loader.load(str(file))

        document.text = TextCleaner.clean(document.text)

        document = MetadataGenerator.generate(document)

        chunks = chunker.split(document)

        print("Document :", document.filename)
        print("Pages    :", document.pages)
        print("Chunks   :", len(chunks))
        print("Metadata :", document.metadata)

        print("\nFirst Chunk:\n")
        print(chunks[0].text[:500])

        print("\nChunk IDs:")

        for chunk in chunks[:5]:
            print(chunk.chunk_number, chunk.id)


if __name__ == "__main__":
    main()