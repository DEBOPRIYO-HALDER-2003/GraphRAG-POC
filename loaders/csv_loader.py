from pathlib import Path

import pandas as pd


class CSVLoader:

    @staticmethod
    def load(file_path: str):

        dataframe = pd.read_csv(file_path)

        return {
            "text": dataframe.to_string(index=False),
            "pages": len(dataframe),
            "filename": Path(file_path).name,
            "filetype": ".csv"
        }