from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="medical-rag-chatbot",
    version="0.1.0",
    author="Daniel Garcia Belman",
    author_email="danielgb331@outlook.com",
    description="RAG-powered medical information system with Ollama + LangChain",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Daniel-jcVv/rag-healthcare-assistant",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.12",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.12",
    ],
)
