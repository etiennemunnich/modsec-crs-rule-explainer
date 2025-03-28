import pytest
from llms.base import LLMProvider
from llms.perplexity import PerplexityProvider
from llms.factory import LLMFactory

def test_llm_factory_create():
    # Test creating a known provider
    provider = LLMFactory.create("perplexity", "test_key")
    assert isinstance(provider, PerplexityProvider)
    
    # Test creating an unknown provider
    with pytest.raises(ValueError):
        LLMFactory.create("unknown_provider", "test_key")

def test_llm_factory_register():
    # Create a test provider class
    class TestProvider(LLMProvider):
        def __init__(self, api_key):
            self.api_key = api_key
            
        def analyze(self, prompt):
            return {"response": "test"}
    
    # Register the new provider
    LLMFactory.register_provider("test", TestProvider)
    
    # Create an instance of the new provider
    provider = LLMFactory.create("test", "test_key")
    assert isinstance(provider, TestProvider)

def test_perplexity_provider():
    # Test initialization
    provider = PerplexityProvider("test_key")
    assert provider.api_key == "test_key"
    assert provider.base_url == "https://api.perplexity.ai"
    
    # Test headers
    assert provider.headers["Authorization"] == "Bearer test_key"
    assert provider.headers["Content-Type"] == "application/json"