from pathlib import Path

import pandas as pd


class XLSXLoader:

    @staticmethod
    def load(file_path: str):

        sheets = pd.read_excel(file_path, sheet_name=None)

        text = ""

        for sheet_name, dataframe in sheets.items():

            text += f"\n\nSheet: {sheet_name}\n"

            text += dataframe.to_string(index=False)

        return {
            "text": text,
            "pages": len(sheets),
            "filename": Path(file_path).name,
            "filetype": ".xlsx"
        }