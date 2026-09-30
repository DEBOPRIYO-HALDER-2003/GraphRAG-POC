from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent

# ------------------------
# Neo4j
# ------------------------

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# ------------------------
# Ollama
# ------------------------

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")

CHAT_MODEL = os.getenv("CHAT_MODEL")
EMBED_MODEL = os.getenv("EMBED_MODEL")

# ------------------------
# Chunking
# ------------------------

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))

# ------------------------
# Directories
# ------------------------

UPLOAD_DIR = BASE_DIR / os.getenv("UPLOAD_DIR")

PROCESSED_DIR = BASE_DIR / os.getenv("PROCESSED_DIR")

VECTORSTORE_DIR = BASE_DIR / os.getenv("VECTORSTORE_DIR")

REGISTRY_FILE = BASE_DIR / os.getenv("REGISTRY_FILE")