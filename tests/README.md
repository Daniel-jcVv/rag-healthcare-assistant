# Tests

Comprehensive test suite for the Medical RAG Chatbot.

## Structure

```
tests/
├── conftest.py              # Pytest fixtures and configuration
├── test_components.py       # Unit tests for individual components
├── test_rag_pipeline.py     # Integration tests for RAG pipeline
└── README.md               # This file
```

## Running Tests

### Run all tests

```bash
pytest
```

### Run with verbose output

```bash
pytest -v
```

### Run specific test file

```bash
pytest tests/test_components.py -v
```

### Run only unit tests (fast)

```bash
pytest -v -m "not slow and not integration"
```

### Run integration tests (requires Ollama + vectorstore)

```bash
pytest -v -m integration
```

### Run with coverage report

```bash
pytest --cov=app --cov-report=html
```

## Test Categories

### Unit Tests
- Fast tests that don't require external services
- Test individual components in isolation
- Located in `test_components.py`

### Integration Tests
- Require Ollama running locally
- Require vectorstore to be created
- Test end-to-end functionality
- Marked with `@pytest.mark.integration`

### Slow Tests
- Tests that take longer to execute
- LLM inference tests
- Marked with `@pytest.mark.slow`

## Prerequisites

### For Unit Tests
```bash
pip install -r requirements.txt
```

### For Integration Tests
1. Install and start Ollama
2. Pull required model:
   ```bash
   ollama pull llama3.2:latest
   ```
3. Create vectorstore:
   ```bash
   python -m app.components.vector_store
   ```

## Test Markers

- `@pytest.mark.unit` - Fast unit tests
- `@pytest.mark.integration` - Tests requiring external services
- `@pytest.mark.slow` - Long-running tests

## Continuous Integration

Tests are automatically run in the CI/CD pipeline via Jenkins.

## Example Output

```
tests/test_components.py::TestPDFLoader::test_pdf_loader_initialization PASSED
tests/test_components.py::TestEmbeddingModel::test_embedding_model_initialization PASSED
tests/test_components.py::TestConfiguration::test_required_env_vars PASSED
tests/test_rag_pipeline.py::test_qa_chain_creation PASSED
tests/test_rag_pipeline.py::test_query_processing PASSED

===================== 5 passed in 2.34s =====================
```
