# Installation Guide

## Overview

This guide walks you through setting up the Medical AI Assistant on your local machine.

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **pip** (comes with Python)
- **Git** ([Download](https://git-scm.com/downloads))
- **HuggingFace Account** ([Sign up](https://huggingface.co/join))

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 4 GB | 8 GB+ |
| Storage | 2 GB | 5 GB+ |
| OS | Linux, macOS, Windows | Linux/macOS |

---

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/medical-ai-assistant.git
cd medical-ai-assistant
```

### 2. Create Virtual Environment

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required packages including:
- LangChain and dependencies
- HuggingFace libraries
- FAISS for vector storage
- Flask for web framework
- And more...

**Expected installation time:** 3-5 minutes

### 4. Get HuggingFace API Token

1. Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
2. Click **"New token"**
3. Set permissions to **"Read"**
4. Copy the generated token

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your token:

```env
HF_TOKEN=hf_your_actual_token_here
HUGGINGFACEHUB_API_TOKEN=hf_your_actual_token_here
```

⚠️ **Important:** Never commit the `.env` file to Git!

### 6. Add Medical Documents

Place your medical PDF documents in the `data/` directory:

```bash
# Example:
cp your_medical_document.pdf data/
```

The project includes a sample medical encyclopedia PDF by default.

### 7. Verify Installation

```bash
python -c "import langchain; import faiss; print('Installation successful!')"
```

If you see "Installation successful!", you're ready to go!

---

## Quick Start

### Process Documents

```bash
python -c "
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.components.embeddings import get_embeddings_model
from app.config.config import DATA_PATH

# Load and process documents
documents = load_pdf_files(DATA_PATH)
chunks = create_text_chunks(documents)
print(f'Processed {len(chunks)} chunks')
"
```

### (Coming Soon) Run the Application

```bash
# Will be available in future version
python app.py
```

---

## Troubleshooting

### Issue: `ModuleNotFoundError`

**Solution:**
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: `FAISS import error`

**Solution:**

For **Linux/macOS:**
```bash
pip install faiss-cpu
```

For **Windows:**
```bash
pip install faiss-cpu --no-cache-dir
```

### Issue: `HuggingFace authentication error`

**Solution:**
- Check that your token is correctly set in `.env`
- Verify token has "Read" permissions
- Try regenerating the token

### Issue: `Out of memory when processing PDFs`

**Solution:**
- Reduce chunk size in `app/config/config.py`:
  ```python
  CHUNCK_SIZE = 300  # Reduced from 500
  ```
- Process fewer documents at once
- Close other applications

### Issue: `PDF parsing error`

**Solution:**
- Ensure PDFs are not encrypted
- Try with a different PDF
- Check PDF file is not corrupted

---

## Development Setup

### Install Development Dependencies

```bash
pip install -r requirements-dev.txt  # (To be created)
```

### Run Tests

```bash
pytest tests/  # (Tests to be implemented)
```

### Code Formatting

```bash
# Format code
black app/

# Check linting
flake8 app/
```

---

## Uninstallation

### Remove Virtual Environment

```bash
# Deactivate first
deactivate

# Remove directory
rm -rf venv/
```

### Clean Up

```bash
# Remove generated files
rm -rf vectorstore/
rm -rf __pycache__/
rm -rf *.egg-info/
```

---

## Docker Installation (Planned)

> **🚧 Coming in v1.5.0**

```bash
# Build image
docker build -t medical-ai-assistant .

# Run container
docker run -p 5000:5000 \
  -e HF_TOKEN=your_token \
  -v $(pwd)/data:/app/data \
  medical-ai-assistant
```

---

## Next Steps

After installation:

1. ✅ Read [Configuration Guide](configuration.md)
2. ✅ Review [Architecture Documentation](../architecture/system-design.md)
3. ✅ Check [Contributing Guide](../development/contributing.md)
4. ✅ Process your first document

---

## Getting Help

- 📖 [Documentation](../README.md)
- 🐛 [Report Issues](https://github.com/yourusername/medical-ai-assistant/issues)
- 💬 [Discussions](https://github.com/yourusername/medical-ai-assistant/discussions)

---

**Document Status:** ✅ Complete
**Last Updated:** October 2025
**Version:** 0.1.0
