import os
HF_TOKEN = os.environ.get("HF_TOKEN")

HUGGINGFACE_REPO_ID = "mistralai/Mistral-78-Instruct-v0.3"
DB_FAISS_PATH = "vectorstore/db_faiss"
DATA_PATH = "data/"
CHUNCK_SIZE = 500
CHUNCK_OVERLAP = 50

