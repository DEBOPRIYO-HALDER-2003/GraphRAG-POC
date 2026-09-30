import re


class TextCleaner:

    @staticmethod
    def clean(text: str):

        text = text.replace("\r", " ")

        text = text.replace("\t", " ")

        text = re.sub(r"\n{3,}", "\n\n", text)

        text = re.sub(r" +", " ", text)

        return text.strip()