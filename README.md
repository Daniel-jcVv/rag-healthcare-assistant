# 🏥 Medical AI Assistant

> **⚠️ Work In Progress** - This project is under active development. Features and documentation are being continuously updated.

A Retrieval-Augmented Generation (RAG) powered medical chatbot designed to provide intelligent medical information retrieval using state-of-the-art LLM technology.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://github.com/langchain-ai/langchain)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-WIP-orange.svg)](https://github.com/yourusername/medical-ai-assistant)

---

## 🎯 Key Highlights

- 📊 **LLMOps Pipeline:** Complete RAG implementation from document ingestion to answer generation
- 🤖 **Production-Ready Architecture:** Modular design with custom exception handling and comprehensive logging
- ⚡ **Efficient Vector Search:** FAISS indexing with semantic embeddings (target: sub-100ms retrieval)
- 🔧 **LLM Integration:** Mistral-7B via HuggingFace API for context-aware medical Q&A
- 📚 **Document Processing:** Intelligent text chunking with overlap for context preservation
- 🎓 **Best Practices:** Environment-based configuration, Git Flow, comprehensive documentation

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Development Progress](#development-progress)
- [Performance Targets](#performance-targets)
- [Technical Deep Dive](#technical-deep-dive)
- [Getting Started](#getting-started)
- [What I Learned](#what-i-learned)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project implements an intelligent medical Q&A system leveraging **Retrieval-Augmented Generation (RAG)** to provide accurate, context-aware responses to medical queries. The system processes medical documents, creates semantic embeddings, and uses vector similarity search to retrieve relevant information before generating responses.

### Key Capabilities

- 📚 **Document Processing**: Ingests and processes medical PDF documents with intelligent chunking
- 🔍 **Semantic Search**: Uses vector embeddings for intelligent information retrieval
- 🤖 **AI-Powered Responses**: Generates contextual answers using LLMs with retrieved context
- ⚡ **Efficient Storage**: FAISS-based vector database for fast similarity search

### Problem Statement

Medical information is vast and complex. This system aims to make medical knowledge more accessible by:
- Processing large medical documents into searchable knowledge bases
- Providing accurate, source-backed answers to medical questions
- Reducing information overload through intelligent retrieval

---

## ✨ Features

### ✅ Completed
- [x] PDF document loader with DirectoryLoader and PyPDFLoader
- [x] Intelligent text chunking (RecursiveCharacterTextSplitter, 500 chars with 50 char overlap)
- [x] HuggingFace embeddings integration (`sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions)
- [x] FAISS vector store configuration with flat L2 index
- [x] Custom exception handling with detailed error messages
- [x] Comprehensive logging system (INFO, WARNING, ERROR levels)
- [x] Environment-based configuration management (python-dotenv)
- [x] Modular application structure following best practices
- [x] Complete technical documentation (Architecture, ADRs, Data Flow)

### 🚧 In Progress
- [ ] Flask REST API endpoints (`/query`, `/health`)
- [ ] Chatbot conversation interface
- [ ] Query processing and retrieval pipeline
- [ ] Response generation with Mistral-7B LLM
- [ ] Context assembly and prompt engineering

### 📅 Planned
- [ ] Web UI with chat interface
- [ ] Conversation history management
- [ ] Multi-document support and metadata tracking
- [ ] Docker containerization
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Unit and integration tests (pytest)
- [ ] Performance optimization and caching
- [ ] CI/CD pipeline with GitHub Actions

---

## 🛠️ Tech Stack

| Category | Technology | Purpose |
|----------|------------|---------|
| **Language** | Python 3.12+ | Core programming language |
| **LLM Framework** | LangChain 0.3 | RAG orchestration and document processing |
| **Embeddings** | HuggingFace Transformers | Semantic text embeddings (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS | Fast similarity search and vector indexing |
| **Web Framework** | Flask | REST API and web interface |
| **LLM Model** | Mistral-7B-Instruct-v0.3 | Answer generation (7B params, 8K context) |
| **Document Processing** | PyPDF, LangChain Loaders | PDF parsing and text extraction |
| **Environment Management** | python-dotenv | Configuration and secrets management |

### Why These Technologies?

- **LangChain:** Mature RAG framework with excellent document utilities and LLM integrations
- **FAISS:** Battle-tested by Meta, fast local vector search, no API costs
- **Mistral-7B:** Strong performance, Apache 2.0 license, efficient 7B params
- **HuggingFace:** Open-source models, easy API integration, cost-effective

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
│   ├── templates/           # Flask templates (future)
│   └── __init__.py
├── data/                    # Medical documents (PDFs)
├── docs/                    # Technical documentation
│   ├── architecture/        # System design, ADRs, data flow
│   ├── setup/              # Installation and configuration
│   └── development/        # Contributing guidelines
├── vectorstore/            # FAISS index storage
│   └── db_faiss/
├── .env                    # Environment variables (gitignored)
├── .gitignore
├── requirements.txt        # Python dependencies
├── setup.py               # Package configuration
└── README.md
```

---

## 📊 Development Progress

### Current Status: **Alpha Development** (v0.1.0-alpha)

```
Overall Progress: ████████░░░░░░░░░░░░ 40%

Core Components:
  ✅ Document Processing      [████████████████████] 100%
  ✅ Embeddings Setup          [████████████████████] 100%
  ✅ Vector Store Config       [████████████████████] 100%
  🚧 API Development           [████████░░░░░░░░░░░░]  40%
  🚧 LLM Integration           [██████░░░░░░░░░░░░░░]  30%
  ⏳ Web Interface             [░░░░░░░░░░░░░░░░░░░░]   0%
  ⏳ Testing Suite             [░░░░░░░░░░░░░░░░░░░░]   0%
```

---

## 📊 Performance Targets

| Metric | Target | Status |
|--------|--------|--------|
| **Query Latency** | < 3 seconds end-to-end | ⏱️ To be measured |
| **Vector Search** | < 100ms for 15K documents | ⏱️ To be measured |
| **Document Processing** | 500 pages/minute | ⏱️ To be measured |
| **Embedding Generation** | < 500ms per query | ⏱️ To be measured |
| **Index Size** | ~45MB for 1500 page encyclopedia | ✅ Achieved |

### Latency Budget (Planned)

```
Total Query Latency: ~3 seconds

Breakdown:
  - Query embedding:      50ms   ( 1.7%)
  - Vector search:        10ms   ( 0.3%)
  - Context assembly:     40ms   ( 1.3%)
  - LLM inference:      2500ms   (83.3%) ← Bottleneck
  - Post-processing:     100ms   ( 3.3%)
  - Network overhead:    300ms   (10.0%)
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
- HuggingFace API token ([Get one here](https://huggingface.co/settings/tokens))
- Virtual environment (recommended)
- 4GB+ RAM, 2GB+ storage

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/medical-ai-assistant.git
cd medical-ai-assistant

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your HuggingFace token

# Run document processing (example)
python -c "
from app.components.pdf_loader import load_pdf_files, create_text_chunks
from app.config.config import DATA_PATH

documents = load_pdf_files(DATA_PATH)
chunks = create_text_chunks(documents)
print(f'✓ Processed {len(chunks)} text chunks')
"
```

### Configuration

Create a `.env` file with:

```env
HF_TOKEN=your_huggingface_token_here
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here
```

⚠️ **Important:** Never commit the `.env` file to Git!

For detailed installation instructions, see [Installation Guide](docs/setup/installation.md).

---

## 📚 What I Learned

This project deepened my understanding of:

### LLMOps & RAG Architecture
- Implementing RAG pipeline from scratch: ingestion → embedding → retrieval → generation
- Vector database design and similarity search optimization with FAISS
- Trade-offs between different chunking strategies and their impact on retrieval quality

### LLM Orchestration
- LangChain framework for document processing and LLM integration
- Prompt engineering for medical domain question answering
- Managing context windows and token budgets for LLM inference

### Production Engineering
- Modular architecture with separation of concerns
- Custom exception handling and comprehensive logging strategies
- Environment-based configuration for different deployment scenarios
- Documentation-driven development with Architecture Decision Records (ADRs)

### Technical Decision-Making
- Evaluating trade-offs: FAISS vs. Pinecone vs. Weaviate vs. ChromaDB
- Model selection: balancing quality, cost, and latency (Mistral-7B vs. GPT-3.5 vs. Llama)
- Embedding model comparison: dimensions vs. speed vs. domain specificity

---

## 🗺️ Roadmap

### Phase 1: Foundation (Current - 40% Complete)
- [x] Project setup and structure
- [x] Document processing pipeline
- [x] Vector database integration
- [x] Technical documentation
- [ ] Basic API endpoints
- [ ] Query processing pipeline

### Phase 2: Core Features (Q4 2025)
- [ ] Complete RAG pipeline with Mistral-7B
- [ ] Conversation management
- [ ] Web interface
- [ ] Error handling improvements
- [ ] Unit tests

### Phase 3: Enhancement (Q1 2026)
- [ ] Performance optimization (caching, async)
- [ ] Multi-model support
- [ ] Advanced search features
- [ ] Docker deployment
- [ ] CI/CD pipeline

### Phase 4: Production Ready (Q2 2026)
- [ ] Comprehensive testing (95%+ coverage)
- [ ] Security hardening (authentication, rate limiting)
- [ ] Complete API documentation (Swagger)
- [ ] Production deployment guide

---

## 🤝 Contributing

This project is currently in early development. Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes using [Conventional Commits](https://www.conventionalcommits.org/) (`git commit -m 'feat: add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

See [Contributing Guide](docs/development/contributing.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Daniel Garcia Belman**
- Email: danielgb331@outlook.com
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

---

## 🙏 Acknowledgments

- Medical encyclopedia data from Gale Encyclopedia of Medicine (Second Edition)
- Built with [LangChain](https://github.com/langchain-ai/langchain) framework
- Embeddings by [HuggingFace](https://huggingface.co/) Transformers
- Vector search powered by [FAISS](https://github.com/facebookresearch/faiss) from Meta AI

---

## 📬 Contact & Support

- 📧 **Email:** danielgb331@outlook.com
- 🐛 **Issues:** [GitHub Issues](https://github.com/yourusername/medical-ai-assistant/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/yourusername/medical-ai-assistant/discussions)

---

<div align="center">

**⭐ Star this repo if you find it interesting!**

*Building the future of medical information retrieval, one commit at a time.*

**Last Updated:** October 2025 | **Version:** 0.1.0-alpha

</div>
