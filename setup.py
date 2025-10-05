from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    ]
else:
    requirements = []

setup(
    name="medical-rag-chatbot",
    version="0.1.0",
    author="Daniel Garcia Belman",
    author_email="danielgb331@outlook.com",
    description="Production RAG data pipeline: ETL for unstructured text, vector database, LLM orchestration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Daniel-jcVv/rag-healthcare-assistant",
    packages=find_packages(exclude=["tests*", "docs*", "scripts*", "custom_jenkins*"]),
    install_requires=requirements,
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Indexing",
        "Operating System :: OS Independent",
    ],
    keywords="rag llm data-pipeline vector-database faiss langchain ollama nlp machine-learning",
    project_urls={
        "Bug Reports": "https://github.com/Daniel-jcVv/rag-healthcare-assistant/issues",
        "Source": "https://github.com/Daniel-jcVv/rag-healthcare-assistant",
        "Documentation": "https://github.com/Daniel-jcVv/rag-healthcare-assistant/tree/main/docs",
        "Docker Hub": "https://hub.docker.com/r/beitmidrash/medical-rag-chatbot",
    },
)
