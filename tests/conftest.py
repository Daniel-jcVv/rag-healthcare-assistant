"""
Pytest Configuration and Fixtures

Shared fixtures and configuration for all tests.
"""

import pytest
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()


@pytest.fixture(scope="session")
def project_root():
    """Return the project root directory"""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def data_path(project_root):
    """Return the data directory path"""
    return project_root / "data"


@pytest.fixture(scope="session")
def vectorstore_path(project_root):
    """Return the vectorstore directory path"""
    return project_root / "vectorstore" / "faiss_index"


@pytest.fixture
def sample_medical_query():
    """Sample medical question for testing"""
    return "What is diabetes?"


@pytest.fixture
def sample_queries():
    """Multiple sample queries for batch testing"""
    return [
        "What is diabetes?",
        "What are the symptoms of hypertension?",
        "How is asthma treated?"
    ]
