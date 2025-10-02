# 🏥 Medical AI Assistant

> **⚠️ Work In Progress** - This project is under active development. Features and documentation are being continuously updated.

A Retrieval-Augmented Generation (RAG) powered medical information system designed to provide intelligent medical knowledge retrieval using state-of-the-art LLM technology.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://github.com/langchain-ai/langchain)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)](https://github.com/Daniel-jcVv/rag-healthcare-assistant)

---

## 🎯 Key Highlights

- 📊 **RAG Pipeline Implementation:** Complete document processing pipeline from PDF ingestion to vector storage
- 🤖 **Production-Ready Architecture:** Modular design with custom exception handling and comprehensive logging
- ⚡ **Efficient Vector Search:** FAISS indexing with semantic embeddings for fast similarity search
- 🔧 **LLM Integration Ready:** Configured for Mistral-7B via HuggingFace API for medical Q&A
- 📚 **Intelligent Document Processing:** Text chunking with overlap for context preservation
- 🎓 **Best Practices:** Environment-based configuration, comprehensive documentation

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Technical Deep Dive](#technical-deep-dive)
- [Getting Started](#getting-started)
- [What I Learned](#what-i-learned)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements the foundational components of an intelligent medical information retrieval system using **Retrieval-Augmented Generation (RAG)**. The system processes medical documents, creates semantic embeddings, and prepares a vector database for efficient similarity search.

### Key Capabilities

- 📚 **Document Processing**: Ingests and processes medical PDF documents with intelligent chunking
- 🔍 **Semantic Embeddings**: Converts text to vector representations using HuggingFace transformers
- 💾 **Vector Storage**: FAISS-based vector database for fast similarity search
- 🛠️ **Modular Architecture**: Clean separation of concerns for maintainability and extensibility

### Problem Statement

Medical information is vast and complex. This system provides the infrastructure to:
- Process large medical documents into searchable knowledge bases
- Enable semantic search over medical content
- Prepare foundation for AI-powered medical Q&A systems

---

## ✨ Features

### ✅ Implemented
- [x] PDF document loader with DirectoryLoader and PyPDFLoader
- [x] Intelligent text chunking (RecursiveCharacterTextSplitter, 500 chars with 50 char overlap)
- [x] HuggingFace embeddings integration (`sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions)
- [x] FAISS vector store configuration with flat L2 index
- [x] Custom exception handling with detailed error messages
- [x] Comprehensive logging system (INFO, WARNING, ERROR levels)
- [x] Environment-based configuration management (python-dotenv)
- [x] Modular application structure following best practices
- [x] Complete technical documentation (Architecture, ADRs, Data Flow)

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Language** | Python 3.12+ | Core programming language |
| **LLM Framework** | LangChain 0.3 | RAG orchestration and document processing |
| **Embeddings** | HuggingFace Transformers | Semantic text embeddings (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS | Fast similarity search and vector indexing |
| **Document Processing** | PyPDF, LangChain Loaders | PDF parsing and text extraction |
| **Environment Management** | python-dotenv | Configuration and secrets management |

### Why These Technologies?

- **LangChain:** Mature RAG framework with excellent document utilities and LLM integrations
- **FAISS:** Battle-tested by Meta, fast local vector search, no API costs
- **sentence-transformers:** Fast inference, good quality embeddings, free and open-source
- **HuggingFace:** Open-source models, easy integration, cost-effective

---

## 📁 Project Structure

```
medical-ai-assistant/
├── app/
│   ├── common/              # Shared utilities
│   │   ├── custom_exception.py
│   │   └── logger.py
│   ├── components/          # Core RAG components
│   │   ├── embeddings.py    # HuggingFace embeddings model
│   │   ├── pdf_loader.py    # Document loading and chunking
│   │   └── vector_store.py  # FAISS vector database
│   ├── config/              # Configuration management
│   │   └── config.py
│   └── __init__.py
├── data/                    # Medical documents (PDFs)
├── docs/                    # Technical documentation
│   ├── architecture/        # System design, ADRs, data flow
│   └── setup/              # Installation and configuration
├── info/                    # Development notes
│   ├── notes.md            # Session notes and progress
│   └── CLAUDE.md           # AI collaboration guidelines
├── vectorstore/            # FAISS index storage
│   └── db_faiss/
├── .env                    # Environment variables (gitignored)
├── .env.example            # Environment template
├── .gitignore
├── LICENSE
├── requirements.txt        # Python dependencies
├── setup.py               # Package configuration
└── README.md
```

---

## 📖 Technical Deep Dive

Comprehensive technical documentation available:

- **[System Architecture](docs/architecture/system-design.md)** - High-level design, components, data flow
- **[Technical Decisions (ADR)](docs/architecture/tech-decisions.md)** - Architecture decision records, trade-offs, alternatives
- **[Data Flow](docs/architecture/data-flow.md)** - Detailed pipeline diagrams, data transformations
- **[Installation Guide](docs/setup/installation.md)** - Step-by-step setup instructions
- **[Configuration Guide](docs/setup/configuration.md)** - Environment variables, tuning parameters

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 or higher
- HuggingFace account (free) - [Sign up here](https://huggingface.co/join)
- 4GB+ RAM, 2GB+ storage

### Installation

```bash
# Clone the repository
git clone https://github.com/Daniel-jcVv/rag-healthcare-assistant.git
cd rag-healthcare-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

1. Create a `.env` file from the example:
```bash
cp .env.example .env
```

2. Get your HuggingFace token:
   - Go to [HuggingFace Settings](https://huggingface.co/settings/tokens)
   - Create a new token with "Read" permissions
   - Copy the token

3. Edit `.env` and add your token:
```env
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```


### Usage

**Process PDF Documents:**
```python
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.config.config import DATA_PATH

# Load PDFs from data directory
documents = load_pdf_files(DATA_PATH)
print(f"Loaded {len(documents)} documents")

# Create text chunks
chunks = create_text_chunks(documents)
print(f"Created {len(chunks)} text chunks")
```

**Generate Embeddings:**
```python
from app.components.embeddings import get_embeddings_model

# Initialize embedding model
embeddings = get_embeddings_model()

# Generate embedding for text
text = "Sample medical text"
vector = embeddings.embed_query(text)
print(f"Embedding dimensions: {len(vector)}")
```

**Vector Store (In Development):**
```python
from app.components.vector_store import create_vector_store

# Create FAISS vector store from chunks
vector_store = create_vector_store(chunks, embeddings)
# Query similar documents (implementation in progress)
```

For detailed instructions, see [Installation Guide](docs/setup/installation.md).



---

## 🔮 Future Enhancements

### Core Features
- Complete vector store implementation with search functionality
- Query processing pipeline with embedding generation
- LLM integration for answer generation (Mistral-7B)
- Context assembly and prompt engineering


### Infrastructure
- Docker containerization
- Unit and integration tests
- Performance optimization and caching
- CI/CD pipeline

### Advanced Features
- Multi-document support with metadata
- Conversation history management
- Advanced search and filtering
- Real-time document updates

---

## 🤝 Contributing

This project is open for contributions. To contribute:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/) (`git commit -m 'feat: add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Daniel Garcia Belman**
- Email: danielgb331@outlook.com
- GitHub: [@Daniel-jcVv](https://github.com/Daniel-jcVv/Daniel-jcVv)
- LinkedIn: [Your LinkedIn](www.linkedin.com/in/daniel-garcía-belman-99a298aa)

---

## 🙏 Acknowledgments

- Grateful to God for wisdom and guidance throughout this project
- Medical encyclopedia data from Gale Encyclopedia of Medicine (Second Edition)
- Built with [LangChain](https://github.com/langchain-ai/langchain) framework
- Embeddings by [HuggingFace](https://huggingface.co/) Transformers
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss) from Meta AI

---

## 📬 Contact & Support

- 📧 **Email:** danielgb331@outlook.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/Daniel-jcVv/rag-healthcare-assistant/issues)

---

<div align="center">

**⭐ Star this repo if you find it interesting!**

*Building intelligent medical information retrieval systems with RAG*

**Last Updated:** October 2025 | **Version:** 0.1.0-alpha

**Soli Deo Gloria (Solo A Dios La Gloria)**

</div>
