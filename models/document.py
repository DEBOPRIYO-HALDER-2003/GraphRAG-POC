from dataclasses import dataclass, field
from typing import Dict


@dataclass
class Document:

    id: str

    filename: str

    filetype: str

    pages: int

    text: str

    metadata: Dict = field(default_factory=dict)