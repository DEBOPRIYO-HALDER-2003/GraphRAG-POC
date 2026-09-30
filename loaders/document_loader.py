from pathlib import Path
import uuid

from models.document import Document

from loaders.csv_loader import CSVLoader
from loaders.docx_loader import DOCXLoader
from loaders.pdf_loader import PDFLoader
from loaders.pptx_loader import PPTXLoader
from loaders.txt_loader import TXTLoader
from loaders.xlsx_loader import XLSXLoader


class DocumentLoader:

    LOADERS = {
        ".pdf": PDFLoader,
        ".docx": DOCXLoader,
        ".txt": TXTLoader,
        ".csv": CSVLoader,
        ".xlsx": XLSXLoader,
        ".pptx": PPTXLoader,
    }

    @classmethod
    def load(cls, file_path: str):

        extension = Path(file_path).suffix.lower()

        if extension not in cls.LOADERS:
            raise ValueError(f"Unsupported file type: {extension}")

        data = cls.LOADERS[extension].load(file_path)

        return Document(
            id=str(uuid.uuid4()),
            filename=data["filename"],
            filetype=data["filetype"],
            pages=data["pages"],
            text=data["text"],
        )