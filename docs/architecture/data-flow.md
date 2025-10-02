# Data Flow Architecture

## Overview

This document describes the data flow within the Medical AI Assistant system, from document ingestion to query response generation.

---

## 1. Document Ingestion Pipeline

### Flow Diagram

```
┌─────────────┐
│  PDF Files  │
│  (Medical   │
│   Docs)     │
└──────┬──────┘
       │
       │ Load
       ▼
┌────────────────────────┐
│  DirectoryLoader       │
│  + PyPDFLoader         │
│                        │
│  - Scans data/ dir     │
│  - Finds *.pdf files   │
│  - Extracts text       │
└──────┬─────────────────┘
       │
       │ Raw Documents
       │ (List[Document])
       ▼
┌────────────────────────┐
│  Text Chunking         │
│  (RecursiveChar        │
│   TextSplitter)        │
│                        │
│  - Chunk size: 500     │
│  - Overlap: 50         │
│  - Preserves context   │
└──────┬─────────────────┘
       │
       │ Text Chunks
       │ (List[Document])
       ▼
┌────────────────────────┐
│  Embedding Generation  │
│  (HuggingFace)         │
│                        │
│  Model: all-MiniLM-L6  │
│  Dims: 384             │
└──────┬─────────────────┘
       │
       │ Embeddings
       │ (Vectors: 384D)
       ▼
┌────────────────────────┐
│  FAISS Vector Store    │
│                        │
│  - Store vectors       │
│  - Build index         │
│  - Save to disk        │
│                        │
│  Path: vectorstore/    │
│        db_faiss        │
└────────────────────────┘
```

### Detailed Steps

#### Step 1: PDF Loading
```python
Input:  data/ directory containing medical PDFs
↓
Process: DirectoryLoader scans for *.pdf files
         PyPDFLoader extracts text page by page
↓
Output: List[Document] with text and metadata
        - page_content: str
        - metadata: {source, page}
```

#### Step 2: Text Chunking
```python
Input:  List[Document] (full documents)
↓
Process: RecursiveCharacterTextSplitter
         - Splits by: ["\n\n", "\n", " ", ""]
         - Chunk size: 500 chars
         - Overlap: 50 chars
         - Preserves word boundaries
↓
Output: List[Document] (chunks)
        - Smaller, manageable pieces
        - Overlapping context preserved
        - Metadata inherited from parent
```

**Example:**
```
Original Document (2000 chars)
        ↓
    Chunking
        ↓
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  Chunk 1    │ │  Chunk 2    │ │  Chunk 3    │ │  Chunk 4    │
│  (0-500)    │ │  (450-950)  │ │  (900-1400) │ │  (1350-1850)│
└─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
     └────────┬────────┘              └────────┬────────┘
           Overlap (50)                     Overlap (50)
```

#### Step 3: Embedding Generation
```python
Input:  Text chunks (strings)
↓
Process: HuggingFace sentence-transformers
         - Model: all-MiniLM-L6-v2
         - Tokenize text
         - Forward pass through model
         - Pool token embeddings
↓
Output: Vector embeddings (float32[384])
        - Dense semantic representation
        - Normalized vectors
```

#### Step 4: Vector Storage
```python
Input:  Embeddings + metadata
↓
Process: FAISS Index Creation
         - Create flat L2 index
         - Add vectors to index
         - Store metadata mapping
↓
Output: Persisted FAISS index
        - vectorstore/db_faiss/index.faiss
        - vectorstore/db_faiss/index.pkl
```

### Data Transformations

```
PDF (Binary)
    ↓ PyPDFLoader
Text (String, ~10,000 chars)
    ↓ TextSplitter
Chunks (List[String], ~500 chars each)
    ↓ Embeddings Model
Vectors (List[float32[384]])
    ↓ FAISS
Indexed Vectors (searchable)
```

### Error Handling

```python
try:
    load_pdf_files()
except FileNotFoundError:
    log.error("Data directory not found")
    return []
except PDFReadError:
    log.error("Failed to parse PDF")
    continue to next file
except Exception:
    log.error("Unexpected error")
    raise CustomException
```

---

## 2. Query Processing Pipeline (Planned)

### Flow Diagram

```
┌─────────────┐
│  User Query │
│  "What is   │
│   diabetes?"│
└──────┬──────┘
       │
       │ Input Validation
       ▼
┌────────────────────────┐
│  Query Processing      │
│                        │
│  - Sanitize input      │
│  - Validate length     │
│  - Preprocess text     │
└──────┬─────────────────┘
       │
       │ Clean Query
       ▼
┌────────────────────────┐
│  Query Embedding       │
│  (same model as docs)  │
│                        │
│  Model: all-MiniLM-L6  │
│  Output: float32[384]  │
└──────┬─────────────────┘
       │
       │ Query Vector
       ▼
┌────────────────────────┐
│  Vector Similarity     │
│  Search (FAISS)        │
│                        │
│  - Compute L2 distance │
│  - Retrieve top-K      │
│  - K = 5 (default)     │
└──────┬─────────────────┘
       │
       │ Top-K Documents
       │ (most relevant)
       ▼
┌────────────────────────┐
│  Context Assembly      │
│                        │
│  - Rank documents      │
│  - Concatenate chunks  │
│  - Format for prompt   │
└──────┬─────────────────┘
       │
       │ Context + Query
       ▼
┌────────────────────────┐
│  Prompt Construction   │
│                        │
│  Template:             │
│  "Given context:       │
│   {context}            │
│   Answer: {query}"     │
└──────┬─────────────────┘
       │
       │ Formatted Prompt
       ▼
┌────────────────────────┐
│  LLM Inference         │
│  (Mistral-7B)          │
│                        │
│  - Send to HF API      │
│  - Generate response   │
│  - Stream tokens       │
└──────┬─────────────────┘
       │
       │ Generated Answer
       ▼
┌────────────────────────┐
│  Post-Processing       │
│                        │
│  - Format response     │
│  - Add citations       │
│  - Validate output     │
└──────┬─────────────────┘
       │
       │ Final Response
       ▼
┌────────────────────────┐
│  Return to User        │
│                        │
│  JSON:                 │
│  {                     │
│    "answer": "...",    │
│    "sources": [...]    │
│  }                     │
└────────────────────────┘
```

### Detailed Query Flow

#### Phase 1: Query Understanding
```
User Input: "What is diabetes?"
      ↓
Validation:
  - Length check (min: 5, max: 500 chars)
  - Character sanitization
  - Language detection (optional)
      ↓
Preprocessed Query: "What is diabetes?"
```

#### Phase 2: Retrieval
```
Query Text
      ↓
Embedding Model (all-MiniLM-L6-v2)
      ↓
Query Vector [v1, v2, ..., v384]
      ↓
FAISS Similarity Search
  - Compute: distance = ||query_vec - doc_vec||
  - Sort by distance (ascending)
  - Select top K=5
      ↓
Retrieved Documents:
  [
    {chunk: "Diabetes is...", score: 0.82, source: "doc1.pdf:p42"},
    {chunk: "Type 2 diabetes...", score: 0.78, source: "doc1.pdf:p43"},
    ...
  ]
```

#### Phase 3: Context Preparation
```
Top-K Documents (5 chunks)
      ↓
Ranking (by relevance score)
      ↓
Concatenation:
  context = "\n\n".join([doc.page_content for doc in top_docs])
      ↓
Context Window Check:
  - Max tokens: 2000 (for 8K model, leaving space for response)
  - Truncate if needed
      ↓
Final Context: "Diabetes is a chronic disease...
                Type 2 diabetes occurs when..."
```

#### Phase 4: Generation
```
Prompt Template:
  """
  You are a medical assistant. Answer the question based on the context.

  Context:
  {context}

  Question: {question}

  Answer:
  """
      ↓
LLM (Mistral-7B) Inference
  - Temperature: 0.7
  - Max tokens: 500
  - Stop sequences: ["\n\nQuestion:", "\n\nContext:"]
      ↓
Generated Answer: "Diabetes is a chronic condition that affects
                   how your body processes blood sugar..."
```

#### Phase 5: Response Formatting
```
Raw LLM Output
      ↓
Post-processing:
  - Remove incomplete sentences
  - Format citations: [1], [2]
  - Add source references
      ↓
Structured Response:
  {
    "answer": "Diabetes is...",
    "sources": [
      {"title": "Gale Medical Encyclopedia", "page": 42},
      ...
    ],
    "confidence": 0.82
  }
```

---

## 3. Data States & Persistence

### Storage Hierarchy

```
Filesystem
├── data/                          # Source documents
│   └── *.pdf                      # Raw PDFs (persistent)
│
├── vectorstore/                   # Vector database
│   └── db_faiss/
│       ├── index.faiss            # Vector index (binary)
│       └── index.pkl              # Metadata (pickle)
│
└── logs/                          # Application logs
    └── app.log                    # Logging output
```

### Data Lifecycle

```
1. INGEST → PDFs loaded into memory (transient)
              ↓
2. PROCESS → Text chunks created (transient)
              ↓
3. EMBED → Vectors generated (transient)
              ↓
4. STORE → Saved to FAISS index (persistent)
              ↓
5. QUERY → Vectors loaded into memory (transient)
              ↓
6. RETRIEVE → Top-K documents returned (transient)
```

---

## 4. Performance Characteristics

### Bottleneck Analysis

```
Document Ingestion:
  PDF Loading:        ████░░░░░░ Fast (I/O bound)
  Text Chunking:      ██████████ Very Fast (CPU)
  Embedding:          ████░░░░░░ Medium (Model inference)
  FAISS Indexing:     ████████░░ Fast (Optimized)

Query Processing:
  Query Embedding:    ██████░░░░ Fast (~50ms)
  Vector Search:      ██████████ Very Fast (~10ms)
  LLM Inference:      ███░░░░░░░ Slow (~2-5s)
  Post-processing:    ██████████ Very Fast
```

### Latency Budget (Target)

```
Total Query Latency: < 3 seconds

Breakdown:
  - Query embedding:     50ms   ( 1.7%)
  - Vector search:       10ms   ( 0.3%)
  - Context prep:        40ms   ( 1.3%)
  - LLM inference:     2500ms   (83.3%)
  - Post-processing:    100ms   ( 3.3%)
  - Network overhead:   300ms   (10.0%)
```

---

## 5. Error Propagation

### Error Handling Strategy

```
Component Failure → Graceful Degradation

PDF Load Error
  ↓
Skip file, log error, continue
  ↓
Return partial results

Embedding Error
  ↓
Retry 3x with exponential backoff
  ↓
If still fails → Use cached embeddings or fail request

FAISS Search Error
  ↓
Log error, return empty results
  ↓
API returns: "No relevant documents found"

LLM API Error
  ↓
Retry with different prompt
  ↓
If fails → Return: "Unable to generate answer, try again"
```

---

## 6. Data Flow Monitoring (Planned)

### Metrics to Track

```python
# Document Ingestion Metrics
- documents_processed: Counter
- chunks_created: Counter
- embedding_time_ms: Histogram
- faiss_index_size_mb: Gauge

# Query Metrics
- queries_per_second: Rate
- query_latency_ms: Histogram
- retrieval_accuracy: Gauge (0-1)
- llm_response_time_ms: Histogram
- cache_hit_rate: Gauge (0-1)

# Error Metrics
- pdf_load_errors: Counter
- embedding_errors: Counter
- llm_api_errors: Counter
- timeout_errors: Counter
```

### Logging Strategy

```python
# Log Levels by Component
INFO:
  - Document loaded: "Loaded document X.pdf (N pages)"
  - Query received: "Processing query: {query}"
  - Response generated: "Generated answer in Nms"

WARNING:
  - Slow operation: "Embedding took >500ms"
  - Partial failure: "Failed to load 1/10 documents"

ERROR:
  - Component failure: "FAISS index corrupted"
  - API error: "HuggingFace API returned 500"

DEBUG:
  - Vector details: "Query vector: [0.12, 0.34, ...]"
  - Retrieved chunks: "Top-K documents: {docs}"
```

---

## Summary

### Key Data Flows

1. **Ingestion:** PDF → Chunks → Embeddings → FAISS
2. **Query:** Question → Embedding → Search → Context → LLM → Answer
3. **Storage:** In-memory processing → Persistent vector store

### Critical Paths

- **Bottleneck:** LLM inference (~83% of latency)
- **Optimization Target:** Caching, batching, faster models
- **Data Persistence:** FAISS index (must backup)

---

**Document Status:** 🚧 Work in Progress
**Last Updated:** October 2025
**Version:** 0.1.0-alpha
