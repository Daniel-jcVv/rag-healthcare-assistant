# System Design - Medical AI Assistant

## Overview

This document describes the high-level architecture of the Medical AI Assistant, a RAG (Retrieval-Augmented Generation) system designed to provide intelligent medical information retrieval and question answering.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    (Flask Web Application)                      │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       API LAYER (Flask)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐         │
│  │   Query      │  │  Document    │  │   Health     │         │
│  │  Endpoint    │  │   Upload     │  │   Check      │         │
│  └──────────────┘  └──────────────┘  └──────────────┘         │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RAG PROCESSING PIPELINE                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  1. Query Understanding & Processing                    │  │
│  │     - Input validation                                  │  │
│  │     - Query preprocessing                               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  2. Retrieval Phase                                     │  │
│  │     - Query embedding generation                        │  │
│  │     - Vector similarity search (FAISS)                  │  │
│  │     - Top-K relevant document retrieval                 │  │
│  └─────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  3. Context Assembly                                    │  │
│  │     - Document ranking                                  │  │
│  │     - Context window management                         │  │
│  │     - Prompt construction                               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                             │                                   │
│                             ▼                                   │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │  4. Generation Phase                                    │  │
│  │     - LLM inference (Mistral-7B)                        │  │
│  │     - Answer generation                                 │  │
│  │     - Response validation                               │  │
│  └─────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌──────────────────┐           ┌──────────────────┐          │
│  │  Vector Store    │           │   Document       │          │
│  │  (FAISS Index)   │◄──────────│   Storage        │          │
│  │                  │           │   (PDFs)         │          │
│  │  - Embeddings    │           │                  │          │
│  │  - Metadata      │           │  - Raw documents │          │
│  │  - Index         │           │  - Chunks        │          │
│  └──────────────────┘           └──────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                            │
│                                                                 │
│  ┌──────────────────┐           ┌──────────────────┐          │
│  │  HuggingFace     │           │   Mistral LLM    │          │
│  │  Embeddings API  │           │   (HF Inference) │          │
│  │                  │           │                  │          │
│  │  Model:          │           │  Model:          │          │
│  │  all-MiniLM-L6-v2│           │  Mistral-7B      │          │
│  └──────────────────┘           └──────────────────┘          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Document Processing Pipeline

**Location:** `app/components/pdf_loader.py`

**Responsibilities:**
- Load PDF documents from the data directory
- Extract text content
- Split documents into manageable chunks
- Maintain document metadata

**Key Functions:**
- `load_pdf_files(data_path)` - Loads all PDFs from specified directory
- `create_text_chunks(documents)` - Splits documents using RecursiveCharacterTextSplitter

**Configuration:**
- Chunk size: 500 characters
- Chunk overlap: 50 characters

### 2. Embedding Generation

**Location:** `app/components/embeddings.py`

**Responsibilities:**
- Initialize HuggingFace embedding model
- Generate vector representations of text
- Handle embedding errors

**Model:** `sentence-transformers/all-MiniLM-L6-v2`
- Dimensions: 384
- Context window: 256 tokens
- Performance: Fast, suitable for semantic search

### 3. Vector Store

**Location:** `app/components/vector_store.py`

**Responsibilities:**
- Store document embeddings
- Perform similarity search
- Retrieve relevant documents

**Technology:** FAISS (Facebook AI Similarity Search)
- Index type: Flat L2
- Storage path: `vectorstore/db_faiss`

### 4. Configuration Management

**Location:** `app/config/config.py`

**Environment Variables:**
- `HF_TOKEN` - HuggingFace API token
- `HUGGINGFACEHUB_API_TOKEN` - Alternative token name

**Configuration Parameters:**
- `HUGGINGFACE_REPO_ID` - LLM model identifier
- `DB_FAISS_PATH` - Vector store location
- `DATA_PATH` - Document directory
- `CHUNK_SIZE` - Document chunk size
- `CHUNK_OVERLAP` - Chunk overlap size

### 5. Common Utilities

**Location:** `app/common/`

**Logger (`logger.py`):**
- Centralized logging configuration
- Log level management
- File and console output

**Custom Exceptions (`custom_exception.py`):**
- Application-specific error handling
- Error message formatting
- Exception chaining

## Data Flow

### Document Ingestion Flow

```
PDF Documents → PyPDFLoader → Text Extraction → Text Chunking
                                                      ↓
FAISS Index ← Store Embeddings ← Generate Embeddings ← Text Chunks
```

### Query Processing Flow (Planned)

```
User Query → Validation → Embedding Generation → Vector Search
                                                       ↓
Response ← LLM Generation ← Context Assembly ← Top-K Documents
```

## Design Patterns

### 1. Modular Architecture
- Clear separation of concerns
- Independent components
- Easy to test and maintain

### 2. Configuration as Code
- Environment-based configuration
- No hardcoded values
- Easy deployment across environments

### 3. Error Handling Strategy
- Custom exception classes
- Comprehensive logging
- Graceful degradation

### 4. Factory Pattern
- `get_embeddings_model()` - Creates embedding model instance
- Centralized object creation
- Easy to swap implementations

## Scalability Considerations

### Current State (MVP)
- Single-threaded processing
- In-memory vector store
- Local file storage

### Future Enhancements
- [ ] Async processing for API endpoints
- [ ] Distributed vector store (Pinecone/Weaviate)
- [ ] Cloud storage integration (S3)
- [ ] Load balancing for multiple LLM requests
- [ ] Caching layer (Redis)
- [ ] Rate limiting and quotas

## Security Considerations

### Current Implementation
- ✅ Environment variables for secrets
- ✅ `.env` excluded from git
- ✅ Input validation in document loaders

### Planned Improvements
- [ ] API authentication (JWT)
- [ ] Request rate limiting
- [ ] Input sanitization for queries
- [ ] CORS configuration
- [ ] HTTPS enforcement

## Performance Metrics (Target)

| Metric | Target | Current Status |
|--------|--------|----------------|
| Document ingestion | < 5 min for 1000 pages | ⏱️ To be measured |
| Query latency | < 2 seconds | ⏱️ To be measured |
| Vector search time | < 100ms | ⏱️ To be measured |
| Embedding generation | < 500ms | ⏱️ To be measured |

## Technology Stack Justification

### Why LangChain?
- Mature RAG framework
- Excellent document processing utilities
- Easy integration with multiple LLMs
- Active community and updates

### Why FAISS?
- Fast similarity search
- Efficient memory usage
- No external dependencies
- Production-ready

### Why HuggingFace?
- Open-source models
- Easy API integration
- Cost-effective
- Flexible model selection

### Why Flask?
- Lightweight and simple
- Easy to learn and deploy
- Sufficient for MVP
- Can migrate to FastAPI later

## Future Architecture Considerations

### Potential Improvements
1. **Microservices Architecture**
   - Separate embedding service
   - Independent LLM service
   - Dedicated vector store service

2. **Event-Driven Architecture**
   - Async document processing
   - Queue-based job management
   - Webhook notifications

3. **Caching Strategy**
   - Query result caching
   - Embedding caching
   - LLM response caching

---

**Document Status:** 🚧 Work in Progress
**Last Updated:** October 2025
**Version:** 0.1.0-alpha
