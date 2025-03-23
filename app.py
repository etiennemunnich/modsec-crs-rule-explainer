import os
import logging
import sys
import traceback
from typing import Dict, Any
import streamlit as st
import requests
import json
from llms.factory import LLMFactory

# Load template from external file
def load_prompt_template():
    try:
        with open('templates/prompt_template.py', 'r') as file:
            return file.read()
    except FileNotFoundError:
        logging.error("Template file not found: templates/prompt_template.py")
        return None

# Failing there is no template, use the prompt
PROMPT_TEMPLATE = load_prompt_template() or """Analyze the following ModSecurity rule (or CRS rule) and provide a detailed explanation of its purpose, 
components, effectiveness, false postives and potential impact. Include any relevant references or documentation: 

Rule for analysis: {rule}"""

# Configure logging
log_level = os.getenv("log_level", "info").lower()
if log_level == "off":
    logging.disable(logging.CRITICAL)
else:
    logging.basicConfig(level=log_level.upper())
logger = logging.getLogger(__name__)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("Loaded environment variables from .env file")
except Exception as e:
    logger.warning(f"Could not load .env file: {e}")

def check_api_key(provider: str = "perplexity") -> str:
    """Check if API key is present in environment variables.
    
    Args:
        provider: The LLM provider to get the API key for
        
    Returns:
        The API key for the specified provider
    """
    key_mapping = {
        "perplexity": "perplexity_api_key"
        # Add new providers here as they become available
    }
    
    env_var = key_mapping.get(provider)
    if not env_var:
        error_msg = f"Unknown provider: {provider}"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    api_key = os.getenv(env_var)
    if not api_key:
        error_msg = f"{env_var} environment variable not found"
        logger.error(error_msg)
        raise ValueError(error_msg)
        
    return api_key

def get_llm_client(api_key: str, provider: str = "perplexity"):
    """Get an LLM client instance."""
    return LLMFactory.create(provider, api_key)

def analyze_modsec_rule(rule: str, prompt_template: str, provider: str = "perplexity") -> Dict[str, Any]:
    """
    Analyze ModSecurity rule using the specified LLM provider.
    
    Args:
        rule: The ModSecurity rule to analyze
        prompt_template: The template to use for formatting the prompt
        provider: The LLM provider to use (default: "perplexity")
    
    Returns:
        Dictionary containing the analysis results
    """
    try:
        logger.info(f"Starting rule analysis with {provider} provider")
        logger.debug(f"Input rule: {rule}")
        
        # Verify API key
        api_key = check_api_key(provider)
        logger.debug(f"API key verified for provider {provider}")
        
        # Initialize LLM client
        client = get_llm_client(api_key, provider)
        
        # Format prompt with rule
        prompt = prompt_template.format(rule=rule)
        logger.debug(f"Formatted prompt: {prompt}")
        
        # Get analysis from LLM
        analysis = client.analyze(prompt)
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing rule: {str(e)}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        raise

def initialize_session_state():
    """Initialize session state variables."""
    if "rule_history" not in st.session_state:
        st.session_state.rule_history = []

def main():
    st.set_page_config(
        page_title="ModSecurity Rule Analyzer",
        page_icon="🛡️",
        layout="wide"
    )

    initialize_session_state()

    st.title("ModSecurity Rule Analyzer 🛡️")
    
    with st.sidebar:
        st.header("Settings")
        provider = st.selectbox(
            "LLM Provider",
            options=["perplexity"],  # Add more providers as they become available
            index=0
        )

    # Main content area
    col1, col2 = st.columns([3, 2])

    with col1:
        st.header("Rule Input")
        rule_input = st.text_area(
            "Enter your ModSecurity rule:",
            height=200,
            help="Paste your ModSecurity rule here for analysis"
        )

        if st.button("Analyze Rule", type="primary"):
            if not rule_input:
                st.error("Please enter a ModSecurity rule to analyze")
            else:
                try:
                    with st.spinner(f"Analyzing rule with {provider} provider..."):
                        logger.info(f"Analyzing rule: {rule_input}")
                        
                        analysis = analyze_modsec_rule(
                            rule_input,
                            PROMPT_TEMPLATE,
                            provider=provider
                        )
                        
                        # Add to history
                        st.session_state.rule_history.append({
                            "rule": rule_input,
                            "analysis": analysis
                        })
                        
                        # Display results
                        st.success("Analysis complete!")
                        
                        with st.expander("Analysis Results", expanded=True):
                            st.write(analysis)
                            
                except Exception as e:
                    st.error(f"Error analyzing rule: {str(e)}")
                    logger.error(f"Error: {str(e)}")
                    logger.debug(f"Stack trace: {traceback.format_exc()}")

    with col2:
        st.header("Analysis History")
        if st.session_state.rule_history:
            for i, entry in enumerate(reversed(st.session_state.rule_history)):
                with st.expander(f"Analysis {len(st.session_state.rule_history) - i}", expanded=False):
                    st.code(entry["rule"], language="apache")
                    st.write(entry["analysis"])
        else:
            st.info("No analysis history yet. Submit a rule to get started!")

if __name__ == "__main__":
    main()