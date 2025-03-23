from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def __init__(self, api_key: str):
        """Initialize the LLM provider with API credentials."""
        pass
    
    @abstractmethod
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """Send a prompt to the LLM and get the response.
        
        Args:
            prompt: The input prompt to send to the LLM
            
        Returns:
            Dictionary containing the LLM response
        """
        pass