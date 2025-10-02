from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="medical-rag-chatbot",
    version="0.1",
    author="Daniel Garcia Belman",
    author_email="danielgb331@outlook.com",
    packages=find_packages(),
    install_requires=requirements,
)
