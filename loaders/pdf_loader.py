from pathlib import Path

from pypdf import PdfReader


class PDFLoader:

    @staticmethod
    def load(file_path: str):

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:
                pages.append(text)

        return {
            "text": "\n".join(pages),
            "pages": len(reader.pages),
            "filename": Path(file_path).name,
            "filetype": ".pdf"
        }