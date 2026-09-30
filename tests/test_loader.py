import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from loaders.document_loader import DocumentLoader

UPLOAD_DIR = PROJECT_ROOT / "data" / "uploads"


def main():

    files = list(UPLOAD_DIR.iterdir())

    if not files:
        print("No documents found.")
        return

    for file in files:

        print("=" * 70)

        print("Loading:", file.name)

        document = DocumentLoader.load(str(file))

        print("Type      :", document["filetype"])
        print("Pages     :", document["pages"])
        print("Characters:", len(document["text"]))

        print("\nPreview:\n")
        print(document["text"][:500])
        print()


if __name__ == "__main__":
    main()