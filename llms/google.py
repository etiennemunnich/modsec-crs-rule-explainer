from typing import Dict, Any
from .base import LLMProvider
import os
import logging

logger = logging.getLogger(__name__)

class GoogleProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key
        logger.debug(f"[GoogleProvider] Initialized with API key: {'set' if bool(api_key) else 'not set'}")

    def analyze(self, prompt: str) -> Dict[str, Any]:
        logger.debug(f"[GoogleProvider] analyze called with prompt: {prompt}")
        response = {"markdown_content": f"[Google] Analysis for: {prompt[:40]}..."}
        logger.debug(f"[GoogleProvider] Returning response: {response}")
        return response 