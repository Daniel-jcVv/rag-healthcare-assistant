from langchain_ollama import OllamaLLM
from app.config.config import OLLAMA_MODEL, OLLAMA_BASE_URL

from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)

def load_llm(model: str = None, base_url: str = None):
    """
    Load Ollama LLM for local inference.

    Args:
        model: Ollama model name (default: from config)
        base_url: Ollama API URL (default: http://localhost:11434)

    Returns:
        OllamaLLM instance
    """
    try:
        model = model or OLLAMA_MODEL
        base_url = base_url or OLLAMA_BASE_URL

        logger.info(f"Loading LLM from Ollama: {model}")

        llm = OllamaLLM(
            model=model,
            base_url=base_url,
            temperature=0.3,  # aleatoriedad (0=deterministic, 1=creative)
            num_predict=256,  # max tokens to generate
        )

        logger.info("LLM loaded successfully from Ollama")
        return llm

    except Exception as e:
        error_message = CustomException("Failed to load LLM from Ollama", e)
        logger.error(str(error_message))
        raise