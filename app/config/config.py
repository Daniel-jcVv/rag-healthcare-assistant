import os

# Ollama Configuration (Local LLM)
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2:latest")
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

# Legacy HuggingFace (deprecated - using Ollama now)
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "gpt2"

# Vector Store Configuration
DB_FAISS_PATH = "vectorstore/db_faiss"
DATA_PATH = "data/"
CHUNCK_SIZE = 500
CHUNCK_OVERLAP = 50

