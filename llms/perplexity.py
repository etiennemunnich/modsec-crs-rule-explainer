# Description: Implementation of LLMProvider for Perplexity AI.
# LLM: Perplexity AI
# Model: sonar-reasoning-pro or sonar-deep-research

from typing import Dict, Any
import requests
from requests.exceptions import JSONDecodeError
from .base import LLMProvider
import logging

logger = logging.getLogger(__name__)

class PerplexityProvider(LLMProvider):
    """Implementation of LLMProvider for Perplexity AI."""
    
    def __init__(self, api_key: str):
        """Initialize the provider with API key.
        
        Args:
            api_key: Perplexity API key
        """
        self.api_key = api_key
        self.base_url = "https://api.perplexity.ai"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        logger.debug(f"[PerplexityProvider] Initialized with API key: {'set' if bool(api_key) else 'not set'}")
        
    def analyze(self, prompt: str) -> Dict[str, Any]:
        logger.debug(f"[PerplexityProvider] analyze called with prompt: {prompt}")
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "sonar-reasoning-pro",
                    "messages": [{
                        "role": "system",
                        "content": "You are a ModSecurity rule analysis expert. Provide detailed analysis following the exact format specified in the prompt, including all sections and subsections. Use markdown formatting for better readability."
                    }, {
                        "role": "user",
                        "content": prompt
                    }],
                    "temperature": 0,
                    "max_tokens": 4096
                },
                timeout=(5.0, 600.0)  # (connect timeout, read timeout)
            )
            
            if not response.ok:
                try:
                    error_json = response.json()
                    error_message = error_json.get('error', {}).get('message', response.text)
                except JSONDecodeError:
                    error_message = response.text or "Unknown error"
                logger.error(f"[PerplexityProvider] API error: {error_message}")
                raise RuntimeError(f"Perplexity API error ({response.status_code}): {error_message}")
            
            response.raise_for_status()
            response_json = response.json()
            
            # Extract the content from the response
            content = response_json.get('choices', [{}])[0].get('message', {}).get('content', '')
            if not content:
                logger.error("[PerplexityProvider] No content received from Perplexity API")
                raise RuntimeError("No content received from Perplexity API")
                
            result = {"markdown_content": content}
            logger.debug(f"[PerplexityProvider] Returning response: {result}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[PerplexityProvider] Request exception: {str(e)}")
            print(f"Request exception details: {str(e)}")
            raise RuntimeError(f"Error calling Perplexity API: {str(e)}")