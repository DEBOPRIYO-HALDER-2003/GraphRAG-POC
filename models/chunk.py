from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Chunk:
    """
    Represents a single chunk of a document.
    """

    id: str

    document_id: str

    chunk_number: int

    text: str

    embedding: Optional[List[float]] = None

    metadata: Dict = field(default_factory=dict)