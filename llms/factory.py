from typing import Dict, Type
from .base import LLMProvider
from .perplexity import PerplexityProvider

class LLMFactory:
    """Factory class for creating LLM provider instances."""
    
    _providers: Dict[str, Type[LLMProvider]] = {
        "perplexity": PerplexityProvider
    }
    
    @classmethod
    def create(cls, provider_name: str, api_key: str) -> LLMProvider:
        """Create an instance of the specified LLM provider.
        
        Args:
            provider_name: Name of the LLM provider to create
            api_key: API key for the provider
            
        Returns:
            An instance of the specified LLM provider
            
        Raises:
            ValueError: If the provider name is not recognized
        """
        provider_class = cls._providers.get(provider_name)
        if provider_class is None:
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        
        return provider_class(api_key)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]):
        """Register a new LLM provider.
        
        Args:
            name: Name to register the provider under
            provider_class: The provider class to register
        """
        cls._providers[name] = provider_class