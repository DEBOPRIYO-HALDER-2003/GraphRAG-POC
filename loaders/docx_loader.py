from pathlib import Path

from docx import Document


class DOCXLoader:

    @staticmethod
    def load(file_path: str):

        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text)

        return {
            "text": "\n".join(paragraphs),
            "pages": 1,
            "filename": Path(file_path).name,
            "filetype": ".docx"
        }