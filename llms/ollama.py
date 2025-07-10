from typing import Dict, Any
from .base import LLMProvider
import os
import logging
import requests

print("OllamaProvider module loaded successfully")

logger = logging.getLogger(__name__)

class OllamaProvider(LLMProvider):
    def __init__(self, api_key: str = None):
        # Ollama does not require an API key, but keep for interface compatibility
        self.api_key = api_key
        self.host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
        self.model = "gemma3:latest"  # Use the latest version of gemma3
        logger.debug(f"[OllamaProvider] Initialized with host: {self.host}, model: {self.model}")

    def _check_server(self):
        url = f"{self.host}/api/tags"
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            logger.debug(f"[OllamaProvider] Ollama server is running: {url}")
        except Exception as e:
            logger.error(f"[OllamaProvider] Ollama server is not running: {e}")
            raise RuntimeError(f"Ollama server is not running at {self.host}. Please start Ollama and try again.")

    def analyze(self, prompt: str) -> Dict[str, Any]:
        logger.debug(f"[OllamaProvider] analyze called with prompt: {prompt}")
        self._check_server()
        url = f"{self.host}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }
        try:
            response = requests.post(url, json=payload, timeout=60)
            response.raise_for_status()
            data = response.json()
            logger.debug(f"[OllamaProvider] Raw response: {data}")
            content = data.get("response", "")
            if not content:
                logger.error("[OllamaProvider] No content received from Ollama API")
                raise RuntimeError("No content received from Ollama API")
            result = {"markdown_content": content}
            logger.debug(f"[OllamaProvider] Returning response: {result}")
            return result
        except Exception as e:
            logger.error(f"[OllamaProvider] Error calling Ollama API: {str(e)}")
            raise RuntimeError(f"Error calling Ollama API: {str(e)}") 