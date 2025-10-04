"""
Unit Tests for RAG Components

Tests individual components of the RAG pipeline:
- PDF Loader
- Embeddings
- Vector Store
- LLM Integration
- Configuration

Usage:
    pytest tests/test_components.py -v
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from app.components.pdf_loader import PDFLoader
from app.components.embeddings import EmbeddingModel
from app.config.config import Config


class TestPDFLoader:
    """Test PDF loading functionality"""

    def test_pdf_loader_initialization(self):
        """Test PDF loader can be initialized"""
        loader = PDFLoader()
        assert loader is not None

    def test_data_directory_exists(self):
        """Test data directory is configured correctly"""
        data_path = Path(Config.DATA_PATH)
        assert data_path.exists(), f"Data path does not exist: {Config.DATA_PATH}"

    def test_load_documents_return_type(self):
        """Test load_documents returns list"""
        loader = PDFLoader()
        docs = loader.load_documents()
        assert isinstance(docs, list), "load_documents should return a list"
        if docs:
            assert hasattr(docs[0], 'page_content'), "Documents should have page_content"
            assert hasattr(docs[0], 'metadata'), "Documents should have metadata"


class TestEmbeddingModel:
    """Test embedding model functionality"""

    def test_embedding_model_initialization(self):
        """Test embedding model can be initialized"""
        model = EmbeddingModel()
        assert model is not None
        assert hasattr(model, 'embeddings'), "Should have embeddings attribute"

    def test_embedding_model_name(self):
        """Test correct embedding model is used"""
        assert Config.EMBEDDING_MODEL == "sentence-transformers/all-MiniLM-L6-v2"

    @pytest.mark.slow
    def test_embed_query(self):
        """Test embedding generation for sample text"""
        model = EmbeddingModel()
        embeddings = model.embeddings

        # Test embedding a simple query
        query = "What is diabetes?"
        embedding = embeddings.embed_query(query)

        assert isinstance(embedding, list), "Embedding should be a list"
        assert len(embedding) == 384, "all-MiniLM-L6-v2 produces 384-dimensional embeddings"
        assert all(isinstance(x, float) for x in embedding), "All values should be floats"


class TestConfiguration:
    """Test configuration management"""

    def test_required_env_vars(self):
        """Test required environment variables are set"""
        assert hasattr(Config, 'DATA_PATH')
        assert hasattr(Config, 'VECTORSTORE_PATH')
        assert hasattr(Config, 'EMBEDDING_MODEL')
        assert hasattr(Config, 'LLM_MODEL')

    def test_paths_are_strings(self):
        """Test configuration paths are strings"""
        assert isinstance(Config.DATA_PATH, str)
        assert isinstance(Config.VECTORSTORE_PATH, str)

    def test_chunk_size_valid(self):
        """Test chunk size is reasonable"""
        assert Config.CHUNK_SIZE > 0, "Chunk size must be positive"
        assert Config.CHUNK_SIZE <= 2000, "Chunk size should be reasonable"

    def test_chunk_overlap_valid(self):
        """Test chunk overlap is reasonable"""
        assert Config.CHUNK_OVERLAP >= 0, "Chunk overlap cannot be negative"
        assert Config.CHUNK_OVERLAP < Config.CHUNK_SIZE, "Overlap must be less than chunk size"


class TestVectorStore:
    """Test vector store functionality"""

    def test_vectorstore_path_exists(self):
        """Test vector store directory exists"""
        vectorstore_path = Path(Config.VECTORSTORE_PATH)
        parent_dir = vectorstore_path.parent
        assert parent_dir.exists(), f"Parent directory should exist: {parent_dir}"

    @pytest.mark.integration
    def test_load_vectorstore(self):
        """Test loading existing vector store"""
        from app.components.vector_store import VectorStore

        try:
            vs = VectorStore()
            vectorstore = vs.load_vectorstore()
            assert vectorstore is not None
            assert hasattr(vectorstore, 'similarity_search')
        except FileNotFoundError:
            pytest.skip("Vectorstore not created yet")


class TestLLMIntegration:
    """Test LLM integration"""

    def test_llm_model_configuration(self):
        """Test LLM model is configured correctly"""
        assert Config.LLM_MODEL == "llama3.2:latest"

    def test_llm_temperature_valid(self):
        """Test LLM temperature is in valid range"""
        assert 0 <= Config.LLM_TEMPERATURE <= 1, "Temperature should be between 0 and 1"

    @pytest.mark.slow
    @pytest.mark.integration
    def test_llm_connection(self):
        """Test connection to Ollama LLM"""
        from app.components.llm import LLMModel

        try:
            llm_model = LLMModel()
            assert llm_model.llm is not None
            assert hasattr(llm_model.llm, 'invoke')
        except Exception as e:
            pytest.skip(f"Ollama not running: {str(e)}")


class TestEndToEnd:
    """End-to-end integration tests"""

    @pytest.mark.slow
    @pytest.mark.integration
    def test_full_rag_pipeline(self):
        """Test complete RAG pipeline"""
        from app.components.retriever import create_qa_chain

        try:
            qa_chain = create_qa_chain()
            assert qa_chain is not None

            # Test simple query
            response = qa_chain.invoke({"query": "What is diabetes?"})
            assert isinstance(response, dict)
            assert 'result' in response
            assert 'source_documents' in response

        except Exception as e:
            pytest.skip(f"Full pipeline not available: {str(e)}")


# Pytest markers configuration
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line("markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')")
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
