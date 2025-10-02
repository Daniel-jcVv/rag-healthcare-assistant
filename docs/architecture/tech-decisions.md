# Technical Decisions & Architecture Decision Records (ADR)

## Overview

This document captures the key technical decisions made during the development of the Medical AI Assistant, including the rationale, alternatives considered, and trade-offs.

---

## ADR-001: Choosing RAG over Fine-Tuning

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need to create a medical Q&A system that provides accurate, up-to-date information from medical documents.

### Decision
Implement a Retrieval-Augmented Generation (RAG) system instead of fine-tuning a base LLM.

### Rationale

**Advantages of RAG:**
- ✅ **No training required** - Faster development and deployment
- ✅ **Easy to update** - Add new documents without retraining
- ✅ **Source attribution** - Can cite specific documents
- ✅ **Cost-effective** - No GPU training costs
- ✅ **Reduced hallucination** - Grounds answers in retrieved documents
- ✅ **Dynamic knowledge** - Knowledge base can be updated in real-time

**Why not Fine-Tuning:**
- ❌ Requires large labeled dataset
- ❌ Expensive and time-consuming training
- ❌ Difficult to update knowledge
- ❌ Risk of catastrophic forgetting
- ❌ Requires specialized hardware (GPUs)

### Alternatives Considered
1. **Fine-tuned medical LLM** - Rejected due to cost and maintenance overhead
2. **Prompt engineering only** - Rejected due to context window limitations
3. **Hybrid approach** - Considered for future enhancement

### Consequences
- Need to maintain vector database
- Query latency includes retrieval time
- Quality depends on document relevance

---

## ADR-002: FAISS as Vector Database

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need a vector database to store and search document embeddings efficiently.

### Decision
Use FAISS (Facebook AI Similarity Search) for local vector storage and similarity search.

### Rationale

**Advantages:**
- ✅ **Fast similarity search** - Optimized for dense vectors
- ✅ **No external dependencies** - Runs locally, no API costs
- ✅ **Battle-tested** - Used in production by Meta
- ✅ **Efficient memory usage** - Handles millions of vectors
- ✅ **Easy integration** - Native LangChain support
- ✅ **Free and open-source**

**Comparison with Alternatives:**

| Feature | FAISS | Pinecone | Weaviate | ChromaDB |
|---------|-------|----------|----------|----------|
| Cost | Free | Paid API | Self-hosted/Cloud | Free |
| Setup | Simple | API only | Complex | Simple |
| Scale | Local limit | Cloud scale | Cloud scale | Medium |
| Speed | Very fast | Fast | Fast | Medium |
| Integration | Excellent | Good | Good | Good |

### Alternatives Considered

1. **Pinecone**
   - ✅ Pros: Managed service, scalable, good DX
   - ❌ Cons: Paid API, vendor lock-in
   - Verdict: Over-engineered for MVP

2. **Weaviate**
   - ✅ Pros: Feature-rich, GraphQL API
   - ❌ Cons: Complex setup, resource-heavy
   - Verdict: Too complex for initial version

3. **ChromaDB**
   - ✅ Pros: Simple, Python-native
   - ❌ Cons: Newer, less proven at scale
   - Verdict: Good alternative, reconsidered for v2

### Consequences
- Vector store is local (not distributed)
- Need backup strategy for FAISS index
- Scaling requires migration to cloud solution
- Perfect for MVP and portfolio demo

### Migration Path
When scaling needs arise:
```
FAISS (local) → ChromaDB (medium scale) → Pinecone/Weaviate (production scale)
```

---

## ADR-003: HuggingFace Embeddings (sentence-transformers)

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need to generate vector embeddings for documents and queries.

### Decision
Use `sentence-transformers/all-MiniLM-L6-v2` from HuggingFace.

### Rationale

**Model Characteristics:**
- **Dimensions:** 384 (compact)
- **Speed:** Very fast inference
- **Quality:** Good for semantic search
- **Size:** 80MB (lightweight)
- **Context:** 256 tokens

**Advantages:**
- ✅ **Free and open-source**
- ✅ **Fast inference** - < 50ms per query
- ✅ **Good accuracy** for general domain
- ✅ **Small model size** - Easy to deploy
- ✅ **Well-documented** - Large community

### Alternatives Considered

1. **OpenAI Embeddings (text-embedding-ada-002)**
   - ✅ Higher quality (1536 dimensions)
   - ❌ Paid API ($0.0001 per 1K tokens)
   - ❌ API dependency and latency
   - Verdict: Cost prohibitive for portfolio

2. **Cohere Embeddings**
   - ✅ Good quality
   - ❌ Paid API
   - Verdict: Similar to OpenAI concerns

3. **Large sentence-transformers models**
   - ✅ Better accuracy
   - ❌ Slower inference
   - ❌ Larger memory footprint
   - Verdict: Overkill for MVP

### Trade-offs
- Medical-specific embeddings might be better
- Could fine-tune embeddings on medical corpus
- Current model is general-purpose

### Future Considerations
- Evaluate medical-specific models (BioBERT, PubMedBERT)
- A/B test with larger models
- Fine-tune on medical terminology

---

## ADR-004: Mistral-7B as LLM

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need an LLM for generating answers based on retrieved context.

### Decision
Use `Mistral-7B-Instruct-v0.3` via HuggingFace Inference API.

### Rationale

**Why Mistral-7B:**
- ✅ **Strong performance** - Outperforms Llama-2-13B
- ✅ **Efficient** - 7B parameters (runs on consumer hardware)
- ✅ **Good instruction following**
- ✅ **Open weights** - Apache 2.0 license
- ✅ **8K context window** - Sufficient for RAG
- ✅ **Active development** - Regular updates

### Alternatives Considered

| Model | Params | Context | License | Pros | Cons |
|-------|--------|---------|---------|------|------|
| **Mistral-7B** | 7B | 8K | Apache 2.0 | Performance, efficiency | - |
| GPT-3.5 | ? | 4K | Proprietary | High quality | Paid API |
| Llama-2-7B | 7B | 4K | Llama 2 | Free | Weaker than Mistral |
| Llama-3-8B | 8B | 8K | Llama 3 | Better than Llama-2 | Commercial restrictions |
| Mixtral-8x7B | 47B | 32K | Apache 2.0 | Best quality | Resource heavy |

### Decision Factors

1. **Cost:** Free via HuggingFace (with rate limits)
2. **Performance:** Excellent for 7B model
3. **License:** Permissive (Apache 2.0)
4. **Deployment:** Can run locally or via API
5. **Community:** Large ecosystem

### Consequences
- Rate limits on HuggingFace API (need to handle)
- May need to self-host for production
- Good enough for MVP and portfolio

### Future Migration Path
```
Mistral-7B (HF API) → Self-hosted Mistral → Mixtral-8x7B → GPT-4 (if budget allows)
```

---

## ADR-005: Flask over FastAPI

**Status:** ✅ Accepted (with future migration planned)

**Date:** September 2025

### Context
Need a web framework for API endpoints and potentially a simple UI.

### Decision
Use Flask for initial development.

### Rationale

**Advantages of Flask:**
- ✅ **Simple and lightweight** - Minimal boilerplate
- ✅ **Mature ecosystem** - 13+ years old
- ✅ **Easy to learn** - Great for MVP
- ✅ **Extensive documentation**
- ✅ **Built-in development server**

**Why not FastAPI (for now):**
- Not needed for synchronous MVP
- Async complexity not required yet
- Flask is sufficient for portfolio demo

### When to Migrate to FastAPI

Migrate when we need:
- [ ] Async/await for concurrent requests
- [ ] Automatic API documentation (OpenAPI)
- [ ] Better performance under load
- [ ] WebSocket support
- [ ] Production deployment

### Migration Complexity
- **Low to Medium** - Similar patterns
- Can coexist during transition
- LangChain supports both

### Consequences
- Synchronous request handling
- Manual API documentation
- Good enough for MVP
- Easy migration path exists

---

## ADR-006: Document Chunking Strategy

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need to split large medical documents into chunks for embedding and retrieval.

### Decision
Use `RecursiveCharacterTextSplitter` with:
- **Chunk size:** 500 characters
- **Chunk overlap:** 50 characters (10%)

### Rationale

**Why RecursiveCharacterTextSplitter:**
- Preserves semantic boundaries
- Respects paragraph structure
- Handles multiple separators hierarchically
- LangChain's recommended approach

**Chunk Size Selection:**

| Size | Pros | Cons | Use Case |
|------|------|------|----------|
| 200-300 | Precise retrieval | Fragmented context | Code, Q&A |
| **500** | **Balanced** | **Good for medical text** | **General docs** |
| 1000+ | Full context | Less precise | Long-form |

**Overlap Rationale:**
- 50 chars (10%) prevents information loss at boundaries
- Captures context spanning chunk breaks
- Minimal redundancy overhead

### Alternatives Considered

1. **Semantic Chunking**
   - ✅ Better context preservation
   - ❌ More complex, slower
   - Verdict: Future enhancement

2. **Fixed Token Chunking**
   - ✅ Predictable for LLM
   - ❌ Breaks mid-sentence
   - Verdict: Too rigid

3. **Sentence-based Chunking**
   - ✅ Clean boundaries
   - ❌ Variable size, complexity
   - Verdict: Over-engineered

### Validation Approach
```python
# Metrics to monitor:
- Average chunk size
- Chunks per document
- Retrieval accuracy
- Context completeness
```

### Future Optimizations
- [ ] Experiment with different chunk sizes
- [ ] A/B test overlap percentages
- [ ] Implement semantic chunking
- [ ] Add metadata (section headers, page numbers)

---

## ADR-007: Environment Configuration Management

**Status:** ✅ Accepted

**Date:** September 2025

### Context
Need secure and flexible configuration management for different environments.

### Decision
Use `python-dotenv` with `.env` files for configuration.

### Rationale

**Advantages:**
- ✅ **12-Factor App methodology** - Config in environment
- ✅ **Security** - Secrets not in code
- ✅ **Flexibility** - Easy per-environment config
- ✅ **Simple** - No complex setup
- ✅ **Standard practice** - Industry norm

### Configuration Strategy

```
.env (local, gitignored)
.env.example (template, committed)
config.py (loader, validation)
```

### Alternatives Considered

1. **YAML Config Files**
   - ❌ Secrets in files
   - ❌ Not 12-factor compliant

2. **AWS Secrets Manager / Vault**
   - ✅ Production-ready
   - ❌ Over-engineered for MVP
   - Future: Use in production

3. **Hardcoded Values**
   - ❌ Security risk
   - ❌ Not rejected for obvious reasons

### Security Practices
- ✅ `.env` in `.gitignore`
- ✅ `.env.example` for documentation
- ✅ Validation in `config.py`
- ✅ No defaults for secrets

---

## Summary of Key Decisions

| Decision | Technology | Status | Rationale |
|----------|-----------|--------|-----------|
| Architecture | RAG | ✅ | Flexibility, cost-effective |
| Vector DB | FAISS | ✅ | Fast, local, free |
| Embeddings | all-MiniLM-L6-v2 | ✅ | Fast, good quality |
| LLM | Mistral-7B | ✅ | Performance, license |
| Web Framework | Flask | ✅ | Simple, MVP-appropriate |
| Chunking | Recursive + 500 chars | ✅ | Balanced approach |
| Config | python-dotenv | ✅ | Secure, standard |

---

## Decision Review Schedule

- **Next Review:** After MVP completion
- **Trigger:** Performance issues or scaling needs
- **Owner:** Development team

---

**Document Status:** 🚧 Living Document
**Last Updated:** October 2025
**Version:** 1.0
