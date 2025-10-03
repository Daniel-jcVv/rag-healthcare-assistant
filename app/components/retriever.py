from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.components.llm import load_llm
from app.components.vector_store import load_vector_store

from app.config.config import OLLAMA_MODEL, OLLAMA_BASE_URL
from app.common.logger import get_logger
from app.common.custom_exception import CustomException
import os 


logger = get_logger(__name__)

CUMTOM_PROMPT_TEMPLATE = """ 
    Answer the following medical question in 2-3 lines maximum 
    using only the information provided in the context.

    Context:
    {context}

    Question: 
    {question}

    Answer:
    """

def set_custom_prompt():
    return PromptTemplate(template=CUMTOM_PROMPT_TEMPLATE, input_variables=["context", "question"])

def create_qa_chain():
    try:
        logger.info("Loading vector store for context")
        db = load_vector_store()
        
        if db is None:
            raise CustomException("Vector store for context")
          
        llm = load_llm(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL)

        if llm is None:
            raise CustomException("LLM not loaded")
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": set_custom_prompt()}
            )
        
        logger.info("Succesfully created QA chain")
        return qa_chain
        
    except Exception as e:
        error_message = CustomException("Failed to create QA chain", e)
        logger.error(str(error_message))
   
