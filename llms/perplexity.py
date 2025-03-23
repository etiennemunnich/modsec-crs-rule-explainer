# Description: Implementation of LLMProvider for Perplexity AI.
# LLM: Perplexity AI
# Model: sonar-reasoning-pro or sonar-deep-research

from typing import Dict, Any
import requests
from requests.exceptions import JSONDecodeError
from .base import LLMProvider

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
        
    def analyze(self, prompt: str) -> Dict[str, Any]:
        """Send a prompt to Perplexity AI and get the response.
        
        Args:
            prompt: The input prompt to send to Perplexity
            
        Returns:
            Dictionary containing the Perplexity response
        """
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers=self.headers,
                json={
                    "model": "sonar-reasoning-pro",
                    "messages": [{"role": "user", "content": prompt}],
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
                raise RuntimeError(f"Perplexity API error ({response.status_code}): {error_message}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Request exception details: {str(e)}")
            raise RuntimeError(f"Error calling Perplexity API: {str(e)}")