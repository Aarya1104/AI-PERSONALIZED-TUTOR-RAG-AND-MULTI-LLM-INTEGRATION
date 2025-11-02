import os
from pathlib import Path

# Directories
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOADS_DIR = BASE_DIR / "uploads"
MODELS_DIR = BASE_DIR / "models"
CHROMA_DB_DIR = DATA_DIR / "chroma_db"
CONVERSATIONS_DIR = DATA_DIR / "conversations"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True, parents=True)
UPLOADS_DIR.mkdir(exist_ok=True, parents=True)
MODELS_DIR.mkdir(exist_ok=True, parents=True)
CHROMA_DB_DIR.mkdir(exist_ok=True, parents=True)
CONVERSATIONS_DIR.mkdir(exist_ok=True, parents=True)

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Chunking Configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Retrieval Configuration
USE_HYBRID_SEARCH = True
HYBRID_ALPHA = 0.5
USE_RERANKING = True
RERANK_TOP_K = 10

# Device Configuration
DEVICE = "cpu"

# Conversation Settings
MAX_HISTORY_LENGTH = 10
ENABLE_CONVERSATION_EXPORT = True

print(f"Configuration loaded. Using device: {DEVICE}", end="\n")
print(f"Hybrid Search: {USE_HYBRID_SEARCH}, Reranking: {USE_RERANKING}", end="\n")
