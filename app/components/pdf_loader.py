import os
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

from app.config.config import DATA_PATH, CHUNCK_SIZE, CHUNCK_OVERLAP

logger = get_logger(__name__)


def load_pdf_files(data_path):
    try:
        if not os.path.exists(DATA_PATH):
            raise CustomException("Data path does not exist")
        logger.info(f"Loading PDF files {DATA_PATH}")

        loader = DirectoryLoader(DATA_PATH, glob="*.pdf", loader_cls=PyPDFLoader)

        documents=loader.load()

        if not documents:
            logger.warning("No pdfs were found")
        else:
            logger.info(f"Succesfully fetched {len(documents)} documents")
        
        return documents
    
    except Exception as e:
        error_message = CustomException("Failed to load PDF files", e)
        logger.error(str(error_message))
        return [] 


def create_text_chunks(documents):
    try:
        if not documents:
            raise CustomException("No documents were found")
        
        logger.info(f"Splitting {len(documents)} documents into chunks")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNCK_SIZE, chunk_overlap=CHUNCK_OVERLAP)
        text_chuncks = text_splitter.split_documents(documents)

        logger.info(f"Generated {len(text_chuncks)} text chunks")
        return text_chuncks
    
    except Exception as e:
        error_message = CustomException("Failed to create text chunks", e)
        logger.error(str(error_message))
        return []


        
        


