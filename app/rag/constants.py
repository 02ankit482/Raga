"""
RAG constants used across loaders, retriever, generator and pipeline.
"""

# =========================
# Chunking
# =========================
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# =========================
# Retrieval
# =========================
TOP_K = 3
max_history_turns = 3
# =========================
# Models
# =========================
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
GENERATION_MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

# =========================
# Generation
# =========================
MAX_NEW_TOKENS = 256
TEMPERATURE = 0.4
