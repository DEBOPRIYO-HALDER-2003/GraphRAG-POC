from pathlib import Path


class TXTLoader:

    @staticmethod
    def load(file_path: str):

        path = Path(file_path)

        with open(path, "r", encoding="utf-8", errors="ignore") as file:
            text = file.read()

        return {
            "text": text,
            "pages": 1,
            "filename": path.name,
            "filetype": ".txt"
        }