from typing import Dict, Type
from .base import LLMProvider
from .perplexity import PerplexityProvider
from .openai import OpenAIProvider
from .xcom import XComProvider
from .google import GoogleProvider
from .ollama import OllamaProvider
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    """Factory class for creating LLM provider instances."""
    
    _providers: Dict[str, Type[LLMProvider]] = {
        "perplexity": PerplexityProvider,
        "openai": OpenAIProvider,
        "xcom": XComProvider,
        "google": GoogleProvider,
        "ollama": OllamaProvider
    }
    
    # Log registered providers on startup
    logger.debug(f"LLMFactory initialized with providers: {list(_providers.keys())}")
    print(f"LLMFactory loaded with providers: {list(_providers.keys())}")
    
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
        logger.debug(f"LLMFactory.create called with provider_name={provider_name}, api_key={'set' if api_key else 'not set'}")
        logger.debug(f"Available providers: {list(cls._providers.keys())}")
        print(f"LLMFactory.create called with provider_name={provider_name}")
        print(f"Available providers: {list(cls._providers.keys())}")
        print(f"Provider name in request: '{provider_name}'")
        print(f"Provider name type: {type(provider_name)}")
        print(f"All provider keys: {[repr(k) for k in cls._providers.keys()]}")
        provider_class = cls._providers.get(provider_name)
        print(f"Provider class found: {provider_class}")
        if provider_class is None:
            logger.error(f"Unknown LLM provider: {provider_name}")
            raise ValueError(f"Unknown LLM provider: {provider_name}")
        logger.debug(f"Instantiating provider class: {provider_class}")
        return provider_class(api_key)
    
    @classmethod
    def register_provider(cls, name: str, provider_class: Type[LLMProvider]):
        """Register a new LLM provider.
        
        Args:
            name: Name to register the provider under
            provider_class: The provider class to register
        """
        cls._providers[name] = provider_class