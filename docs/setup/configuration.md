# Configuration Guide

## Overview

This guide explains how to configure the Medical AI Assistant for your specific needs.

---

## Configuration Files

### 1. Environment Variables (`.env`)

**Location:** Project root

```env
# HuggingFace Authentication
HF_TOKEN=hf_your_token_here
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here

# Optional: Logging Level
LOG_LEVEL=INFO

# Optional: Flask Settings
FLASK_ENV=development
FLASK_DEBUG=True
```

### 2. Application Configuration (`app/config/config.py`)

**Location:** `app/config/config.py`

```python
import os

# API Tokens
HF_TOKEN = os.environ.get("HF_TOKEN")

# Model Configuration
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Vector Store Settings
DB_FAISS_PATH = "vectorstore/db_faiss"

# Data Settings
DATA_PATH = "data/"

# Text Processing
CHUNCK_SIZE = 500
CHUNCK_OVERLAP = 50
```

---

## Configuration Parameters

### Model Settings

#### LLM Model

```python
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"
```

**Available alternatives:**
- `"mistralai/Mistral-7B-Instruct-v0.3"` - Default, balanced
- `"mistralai/Mixtral-8x7B-Instruct-v0.1"` - Better quality, slower
- `"meta-llama/Llama-2-7b-chat-hf"` - Alternative option
- `"HuggingFaceH4/zephyr-7b-beta"` - Good instruction following

**Considerations:**
- Larger models = better quality but slower
- Some models require approval from HuggingFace
- Check model licenses for commercial use

#### Embedding Model

**Location:** `app/components/embeddings.py`

```python
model_name = "sentence-transformers/all-MiniLM-L6-v2"
```

**Alternatives:**
- `"sentence-transformers/all-MiniLM-L6-v2"` - Fast, 384 dims (Default)
- `"sentence-transformers/all-mpnet-base-v2"` - Better quality, 768 dims
- `"BAAI/bge-small-en-v1.5"` - Optimized for retrieval
- `"dmis-lab/biobert-v1.1"` - Medical-specific (requires fine-tuning)

**To change:**
```python
# In app/components/embeddings.py
model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)
```

### Text Processing Settings

#### Chunk Size

```python
CHUNCK_SIZE = 500  # characters
```

**Guidelines:**
- **Small (200-300):** Precise retrieval, fragmented context
- **Medium (400-600):** Balanced (recommended)
- **Large (800-1000):** More context, less precise

**Example use cases:**
```python
# For short Q&A
CHUNCK_SIZE = 300

# For detailed explanations
CHUNCK_SIZE = 800
```

#### Chunk Overlap

```python
CHUNCK_OVERLAP = 50  # characters (10% of chunk size)
```

**Best practices:**
- Overlap = 10-20% of chunk size
- Too small: Lost context at boundaries
- Too large: Redundant storage

**Examples:**
```python
CHUNCK_SIZE = 500
CHUNCK_OVERLAP = 50   # 10% - Recommended

CHUNCK_SIZE = 1000
CHUNCK_OVERLAP = 150  # 15% - For large chunks
```

### Vector Store Settings

#### Storage Path

```python
DB_FAISS_PATH = "vectorstore/db_faiss"
```

**Notes:**
- Path is relative to project root
- Directory created automatically
- Backup this directory for data persistence

**Custom path:**
```python
DB_FAISS_PATH = "/absolute/path/to/vectorstore"
```

#### FAISS Index Type (Advanced)

**Current:** Flat L2 (exact search)

**For large datasets (>100k vectors):**
```python
# In app/components/vector_store.py (to be implemented)
import faiss

# IVF index for faster approximate search
index = faiss.IndexIVFFlat(quantizer, dimension, nlist)
```

### Data Settings

#### Document Directory

```python
DATA_PATH = "data/"
```

**Notes:**
- Only PDF files are processed
- Subdirectories not scanned (yet)
- Files must be readable (not encrypted)

**Multiple directories (future):**
```python
DATA_PATHS = [
    "data/medical_books/",
    "data/research_papers/",
    "data/guidelines/"
]
```

---

## Environment-Specific Configuration

### Development Environment

```env
# .env.development
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
CHUNCK_SIZE=300  # Faster processing for testing
```

### Production Environment

```env
# .env.production
FLASK_ENV=production
FLASK_DEBUG=False
LOG_LEVEL=WARNING
CHUNCK_SIZE=500
```

---

## Logging Configuration

### Log Levels

Available levels: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`

**Set in `.env`:**
```env
LOG_LEVEL=INFO
```

**Default behavior:**
```python
# app/common/logger.py
INFO: General operations
WARNING: Potential issues
ERROR: Operation failures
DEBUG: Detailed information (development only)
```

### Log Output

**Console output (default):**
```
2025-10-02 08:30:15 - INFO - Loading PDF files from data/
2025-10-02 08:30:16 - INFO - Successfully fetched 1500 documents
```

**File output (future):**
```python
# Add to logger.py
handler = logging.FileHandler('logs/app.log')
logger.addHandler(handler)
```

---

## Performance Tuning

### For Limited RAM (< 8GB)

```python
# Reduce chunk size
CHUNCK_SIZE = 300
CHUNCK_OVERLAP = 30

# Use smaller embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dims
```

### For Speed Optimization

```python
# Increase chunk size (fewer chunks)
CHUNCK_SIZE = 800
CHUNCK_OVERLAP = 80

# Use faster embedding model
model_name = "sentence-transformers/all-MiniLM-L6-v2"
```

### For Better Accuracy

```python
# Optimal chunk size
CHUNCK_SIZE = 500
CHUNCK_OVERLAP = 75

# Better embedding model
model_name = "sentence-transformers/all-mpnet-base-v2"  # 768 dims
```

---

## Security Configuration

### API Tokens

**Never commit tokens to Git:**
```bash
# .gitignore should contain:
.env
.env.*
*.key
*.pem
```

**Token rotation:**
1. Generate new token at HuggingFace
2. Update `.env` file
3. Restart application

### File Permissions

**Linux/macOS:**
```bash
chmod 600 .env  # Owner read/write only
chmod 700 vectorstore/  # Owner full access only
```

---

## Advanced Configuration

### Custom Exception Messages

**Location:** `app/common/custom_exception.py`

```python
class CustomException(Exception):
    def __init__(self, message, original_exception=None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)
```

### Retry Configuration (Future)

```python
# For API calls
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds
BACKOFF_FACTOR = 2  # exponential backoff
```

---

## Configuration Validation

### Check Configuration

```python
# Run this to validate your setup
python -c "
from app.config.config import *

assert HF_TOKEN is not None, 'HF_TOKEN not set'
assert CHUNCK_SIZE > 0, 'Invalid CHUNCK_SIZE'
assert CHUNCK_OVERLAP < CHUNCK_SIZE, 'Overlap too large'

print('✓ Configuration valid')
"
```

### Common Issues

**Issue: `HF_TOKEN is None`**
```bash
# Solution: Check .env file exists and is loaded
source venv/bin/activate
python -c "import os; print(os.environ.get('HF_TOKEN'))"
```

**Issue: FAISS path not accessible**
```bash
# Solution: Create directory
mkdir -p vectorstore/db_faiss
chmod 755 vectorstore
```

---

## Configuration Best Practices

### ✅ Do's

- ✅ Use environment variables for secrets
- ✅ Keep `.env.example` updated
- ✅ Document configuration changes
- ✅ Use different configs for dev/prod
- ✅ Validate configuration on startup

### ❌ Don'ts

- ❌ Commit `.env` to Git
- ❌ Hardcode API tokens in code
- ❌ Share tokens publicly
- ❌ Use production tokens in development
- ❌ Ignore configuration errors

---

## Configuration Templates

### Minimal Configuration (`.env.example`)

```env
# Required
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

# Optional
LOG_LEVEL=INFO
```

### Full Configuration (`.env.full.example`)

```env
# === HuggingFace Authentication ===
HF_TOKEN=your_token_here
HUGGINGFACEHUB_API_TOKEN=your_token_here

# === Application Settings ===
FLASK_ENV=development
FLASK_DEBUG=True
LOG_LEVEL=INFO

# === Model Configuration ===
# Uncomment to override defaults
# HUGGINGFACE_REPO_ID=mistralai/Mistral-7B-Instruct-v0.3
# EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# === Data Processing ===
# CHUNCK_SIZE=500
# CHUNCK_OVERLAP=50
# DATA_PATH=data/

# === Storage ===
# DB_FAISS_PATH=vectorstore/db_faiss
```

---

## Next Steps

After configuration:

1. ✅ Test your setup: `python -c "from app.config.config import *; print('OK')"`
2. ✅ Process documents
3. ✅ Review [Architecture Documentation](../architecture/system-design.md)
4. ✅ Start development

---

**Document Status:** ✅ Complete
**Last Updated:** October 2025
**Version:** 0.1.0
