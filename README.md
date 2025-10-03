# 🏥 Medical AI Assistant

> **Portfolio Project:** A production-ready RAG system demonstrating advanced LLM, vector search, and full-stack development skills.

A privacy-first, Retrieval-Augmented Generation (RAG) powered medical information system that processes 759 pages of medical literature to provide intelligent, source-cited answers using local LLM inference.

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-green.svg)](https://github.com/langchain-ai/langchain)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-green.svg)](https://github.com/Daniel-jcVv/rag-healthcare-assistant)

---

## 🎯 Key Highlights

- 📊 **RAG Pipeline Implementation:** Complete document processing pipeline from PDF ingestion to vector storage
- 🤖 **Production-Ready Architecture:** Modular design with custom exception handling and comprehensive logging
- ⚡ **Efficient Vector Search:** FAISS indexing with semantic embeddings for fast similarity search
- 🔧 **Local LLM Integration:** Uses Ollama with Llama 3.2 for privacy-focused, cost-free medical Q&A
- 💬 **Modern Web UI:** Responsive chat interface with source citation display
- 📚 **Intelligent Document Processing:** Text chunking with overlap for context preservation
- 🎓 **Best Practices:** Environment-based configuration, comprehensive documentation

---

## 📋 Table of Contents

- [Demo](#demo)
- [Performance Metrics](#performance-metrics)
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

## 🎬 Demo

### Sample Query & Response

**Question:** "What is diabetes?"

**Answer:**
> Diabetes mellitus is a condition in which the pancreas no longer produces enough insulin or when cells become resistant to insulin, leading to high blood glucose levels.

**Sources Cited:**
1. The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf (Page 436)
2. The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf (Page 435)
3. The_GALE_ENCYCLOPEDIA_of_MEDICINE_SECOND.pdf (Page 441)

**Response Time:** ~10 seconds (local CPU inference)

> 📹 **[Demo Video/GIF Coming Soon]** - Recording a screencast of the chat interface in action.

---

## 📊 Performance Metrics

### System Capabilities

| Metric | Value | Details |
|--------|-------|---------|
| **Document Processing** | 759 pages → 7,080 chunks | ~45 seconds total processing time |
| **Vector Store Size** | 15.2 MB | FAISS index with 7,080 document chunks |
| **Search Latency** | <100ms | Vector similarity search in FAISS |
| **Query Response Time** | 8-12 seconds | End-to-end (search + LLM inference) |
| **Embedding Dimensions** | 384 | all-MiniLM-L6-v2 model |
| **LLM Parameters** | 3 billion | Llama 3.2 (local inference) |
| **Chunk Size** | 500 characters | 10% overlap (50 chars) |

### Performance Breakdown

```
Total Response Time: ~10 seconds
├─ Vector Search (FAISS):     0.1s  (1%)
├─ Context Preparation:       0.05s (0.5%)
├─ LLM Inference (Ollama):    9.8s  (98%)
└─ Response Formatting:       0.05s (0.5%)
```

**Why 10 seconds?**
- Local CPU inference (no GPU required)
- 3B parameter model generating ~100 tokens
- Trade-off: 3x slower than cloud APIs but **$0 cost** and **100% private**

### Accuracy & Quality

- ✅ **Source-grounded answers:** Every response cites specific documents and pages
- ✅ **Medical accuracy:** Answers verified against medical encyclopedia sources
- ✅ **Concise responses:** Configured for 2-3 line answers (customizable)
- ✅ **Context-aware:** Uses retrieved chunks for accurate, relevant information

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
- [x] Local LLM integration with Ollama (Llama 3.2)
- [x] Flask web application with RESTful API
- [x] Responsive chat UI with typing indicators and source citations
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
| **Local LLM** | Ollama + Llama 3.2 | Privacy-focused, cost-free inference |
| **Embeddings** | HuggingFace Transformers | Semantic text embeddings (all-MiniLM-L6-v2) |
| **Vector Store** | FAISS | Fast similarity search and vector indexing |
| **Web Framework** | Flask 3.1 | RESTful API and web interface |
| **Document Processing** | PyPDF, LangChain Loaders | PDF parsing and text extraction |
| **Environment Management** | python-dotenv | Configuration and secrets management |

### Why These Technologies?

- **LangChain:** Mature RAG framework with excellent document utilities and LLM integrations
- **Ollama + Llama 3.2:** 100% local, privacy-focused, no API costs, optimized for RAG tasks
- **FAISS:** Battle-tested by Meta, fast local vector search, no API costs
- **sentence-transformers:** Fast inference, good quality embeddings, free and open-source
- **Flask:** Lightweight, easy to deploy, perfect for MVPs and prototypes

---

## 📁 Project Structure

```
medical-ai-assistant/
├── app/
│   ├── common/              # Shared utilities
│   │   ├── custom_exception.py
│   │   └── logger.py
│   ├── components/          # Core RAG components
│   │   ├── data_loader.py   # Pipeline orchestration
│   │   ├── embeddings.py    # HuggingFace embeddings model
│   │   ├── llm.py           # Ollama LLM integration
│   │   ├── pdf_loader.py    # Document loading and chunking
│   │   ├── retriever.py     # QA chain creation
│   │   └── vector_store.py  # FAISS vector database
│   ├── config/              # Configuration management
│   │   └── config.py
│   ├── static/              # Static assets
│   │   ├── css/style.css    # Application styles
│   │   └── js/chat.js       # Chat interface logic
│   ├── templates/           # HTML templates
│   │   └── index.html       # Chat UI
│   ├── application.py       # Flask application
│   └── __init__.py
├── data/                    # Medical documents (PDFs)
├── docs/                    # Technical documentation
│   ├── architecture/        # System design, ADRs, data flow
│   └── setup/              # Installation and configuration
├── info/                    # Development notes
│   ├── debug_guide.md      # Debugging case studies
│   ├── notes.md            # Session notes and progress
│   └── CLAUDE.md           # AI collaboration guidelines
├── logs/                   # Application logs
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
- **Ollama** installed ([installation guide](https://ollama.com/download))
- 8GB+ RAM (recommended), 4GB+ storage
- (Optional) HuggingFace account for embeddings token

### Quick Start

#### 1. Install Ollama and Model

```bash
# Install Ollama (Linux/macOS)
curl -fsSL https://ollama.com/install.sh | sh

# Download Llama 3.2 model (2GB)
ollama pull llama3.2:latest

# Verify Ollama is running
ollama list
```

#### 2. Clone and Setup Project

```bash
# Clone the repository
git clone https://github.com/Daniel-jcVv/rag-healthcare-assistant.git
cd medical-rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env (Ollama config is already set with defaults)
# Optional: Add HuggingFace token for embeddings
```

#### 4. Process Medical Documents

```bash
# Place your PDF files in data/ directory
# Then process them into vector store:
python -m app.components.data_loader
```

#### 5. Run the Application

```bash
# Start Flask server
python -m app.application

# Open browser to http://localhost:5000
```

### Usage Examples

**Ask Medical Questions:**

Open http://localhost:5000 and ask questions like:
- "What is diabetes?"
- "What are the symptoms of hypertension?"
- "How is asthma treated?"

The system will:
1. Search the vector store for relevant medical document chunks
2. Send context + question to Ollama (Llama 3.2)
3. Display the answer with source citations

**API Endpoint:**

```bash
curl -X POST http://localhost:5000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "What is diabetes?"}'
```

Response:
```json
{
  "success": true,
  "answer": "Diabetes mellitus is a chronic disease...",
  "sources": [
    {"document": "medical_encyclopedia.pdf", "page": "435"}
  ]
}
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
- LinkedIn: [My LinkenIn Profile](www.linkedin.com/in/daniel-garcía-belman-99a298aa)

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
