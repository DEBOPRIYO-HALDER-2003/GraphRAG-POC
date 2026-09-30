from pathlib import Path
from datetime import datetime
import uuid


class MetadataGenerator:

    @staticmethod
    def generate(document):

        if not getattr(document, "id", None):
            document.id = str(uuid.uuid4())

        suffix = Path(document.filename).suffix

        document.metadata = {
            "document_id": document.id,
            "filename": document.filename,
            "extension": suffix,
            "pages": document.pages,
            "characters": len(document.text),
            "processed_at": datetime.now().isoformat(),
        }

        return document