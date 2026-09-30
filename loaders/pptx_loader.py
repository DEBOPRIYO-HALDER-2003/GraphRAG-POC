from pathlib import Path

from pptx import Presentation


class PPTXLoader:

    @staticmethod
    def load(file_path: str):

        presentation = Presentation(file_path)

        slides = []

        for slide in presentation.slides:

            slide_text = []

            for shape in slide.shapes:

                if hasattr(shape, "text"):

                    text = shape.text.strip()

                    if text:
                        slide_text.append(text)

            slides.append("\n".join(slide_text))

        return {
            "text": "\n\n".join(slides),
            "pages": len(presentation.slides),
            "filename": Path(file_path).name,
            "filetype": ".pptx"
        }