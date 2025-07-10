import os
import logging
import traceback
from typing import Dict, Any
import streamlit as st
from llms.factory import LLMFactory
from templates.prompt_template import PROMPT_TEMPLATE

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
        "perplexity": "perplexity_api_key",
        "openai": "openai_api_key",
        "xcom": "xcom_api_key",
        "google": "google_api_key"
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
    logger.debug(f"get_llm_client called with provider={provider}, api_key={'set' if api_key else 'not set'}")
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
        logger.debug(f"Instantiating LLM client for provider: {provider}")
        client = get_llm_client(api_key, provider)
        logger.debug(f"LLM client instantiated: {client}")
        
        # Format prompt with rule
        prompt = prompt_template.format(rule=rule)
        logger.debug(f"Formatted prompt: {prompt}")
        
        # Get analysis from LLM
        logger.debug(f"Calling analyze on LLM client for provider: {provider}")
        analysis = client.analyze(prompt)
        logger.debug(f"Received analysis from provider {provider}: {analysis}")
        return analysis
        
    except Exception as e:
        logger.error(f"Error analyzing rule: {str(e)}")
        logger.debug(f"Stack trace: {traceback.format_exc()}")
        raise

def initialize_session_state():
    """Initialize session state variables."""
    if "rule_history" not in st.session_state:
        st.session_state.rule_history = []
    if "current_rule" not in st.session_state:
        st.session_state.current_rule = ""
    if "current_analysis" not in st.session_state:
        st.session_state.current_analysis = None

def main():
    st.set_page_config(
        page_title="ModSecurity Rule Analyzer",
        page_icon="🛡️",
        layout="wide"
    )

    initialize_session_state()

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    html, body, [class*="st-"], [class*="css-"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Reduce top spacing */
    .main .block-container {
        padding-top: 0.5rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Reduce header margins */
    .stMarkdown {
        margin-top: 0 !important;
    }
    
    /* Reduce spacing above title */
    h1, h2, h3 {
        margin-top: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- Sidebar ---
    with st.sidebar:
        st.header("Settings")
        provider = st.selectbox(
            "LLM Provider",
            options=["perplexity", "ollama"],
            index=0
        )
        
        st.header("Quick Start")
        st.markdown("""
        **How to use:**
        1. Paste a ModSecurity rule in the text area.
        2. Click "Analyze Rule".
        3. Review the detailed analysis.
        """)
        
        # Example rules for quick testing
        st.header("Example Rules")
        example_rules = {
            "Scanner Detection": """SecRule REQUEST_HEADERS:User-Agent "@rx (?:acunetix|analyze|audit|black|scan|nikto)" \\
    "id:949110,\\
    phase:2,\\
    block,\\
    t:none,t:lowercase,\\
    log,\\
    msg:'Scanner Detection - Security Scanner Identified',\\
    logdata:'%{MATCHED_VAR}',\\
    tag:'scanner',\\
    severity:'CRITICAL',\\
    ver:'OWASP_CRS/3.3.2',\\
    setvar:'tx.anomaly_score_pl1=+%{tx.critical_anomaly_score}'" """,
            
            "SQL Injection": """SecRule ARGS "@rx (?i:(?:union(?:.*?)select|select(?:.*?)from|insert(?:.*?)into|delete(?:.*?)from|update(?:.*?)set))" \\
    "id:942100,\\
    phase:2,\\
    block,\\
    t:none,t:lowercase,\\
    log,\\
    msg:'SQL Injection Attack Detected',\\
    logdata:'%{MATCHED_VAR}',\\
    tag:'attack-sqli',\\
    severity:'CRITICAL',\\
    ver:'OWASP_CRS/3.3.2'" """,
            
            "XSS Attack": """SecRule ARGS "@rx (?i:<script[^>]*>.*?</script>|<[^>]*javascript:|<[^>]*onload=|<[^>]*onerror=)" \\
    "id:941100,\\
    phase:2,\\
    block,\\
    t:none,t:lowercase,\\
    log,\\
    msg:'XSS Attack Detected',\\
    logdata:'%{MATCHED_VAR}',\\
    tag:'attack-xss',\\
    severity:'CRITICAL',\\
    ver:'OWASP_CRS/3.3.2'" """
        }
        
        selected_example = st.selectbox(
            "Load example rule:",
            ["Select an example..."] + list(example_rules.keys())
        )
        
        if selected_example != "Select an example...":
            st.session_state.current_rule = example_rules[selected_example]
            st.session_state.current_analysis = None # Clear previous analysis

        # Analysis History
        st.header("Analysis History")
        if not st.session_state.rule_history:
            st.info("No analysis history yet.")
        else:
            for i, entry in enumerate(reversed(st.session_state.rule_history)):
                rule_snippet = entry["rule"].splitlines()[0][:40] if entry["rule"] else ""
                if st.button(f"Analysis {len(st.session_state.rule_history) - i}: `{rule_snippet}...`", key=f"history_{i}", use_container_width=True):
                    st.session_state.current_rule = entry["rule"]
                    st.session_state.current_analysis = entry["analysis"]
                    st.rerun() # Rerun to update the main view

        # --- Main Content ---
    st.title("🛡️ ModSecurity Rule Analyzer")
    st.markdown("Analyze ModSecurity rules using AI to understand their purpose, effectiveness, and potential improvements.")

    st.header("Rule Input")
    st.info("""
    **Instructions:** Paste your ModSecurity rule below or load an example from the sidebar.
    The rule should follow the standard ModSecurity syntax: `SecRule VARIABLES "OPERATOR" "ACTIONS"`
    """)

    rule_input = st.text_area(
        "Enter your ModSecurity rule:",
        value=st.session_state.current_rule,
        height=200,
        help="Paste your ModSecurity rule here for analysis. Use the examples in the sidebar for quick testing.",
        placeholder="SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\"",
        key="rule_input_area"
    )
    
    # If user edits the text area, it's a new rule
    if rule_input != st.session_state.current_rule:
        st.session_state.current_rule = rule_input
        st.session_state.current_analysis = None

    col1, col2 = st.columns(2)
    with col1:
        analyze_button = st.button("Analyze Rule", type="primary", use_container_width=True)
    with col2:
        if st.button("Clear Input", use_container_width=True):
            st.session_state.current_rule = ""
            st.session_state.current_analysis = None
            st.rerun()

    if analyze_button:
        if not st.session_state.current_rule.strip():
            st.error("Please enter a ModSecurity rule to analyze")
        else:
            try:
                logger.debug(f"UI selected provider: {provider}")
                with st.spinner(f"Analyzing rule with {provider} provider..."):
                    logger.info(f"Analyzing rule: {st.session_state.current_rule}")
                    analysis = analyze_modsec_rule(
                        st.session_state.current_rule,
                        PROMPT_TEMPLATE,
                        provider=provider
                    )
                    st.session_state.current_analysis = analysis
                    if not any(h['rule'] == st.session_state.current_rule for h in st.session_state.rule_history):
                        st.session_state.rule_history.append({
                            "rule": st.session_state.current_rule,
                            "analysis": analysis
                        })
            except Exception as e:
                st.session_state.current_analysis = None  # Clear any previous analysis
                st.error(f"Error analyzing rule: {str(e)}")
                logger.error(f"Error: {str(e)}")
                logger.debug(f"Stack trace: {traceback.format_exc()}")

    # --- Analysis Results ---
    if st.session_state.current_analysis:
        st.header("Analysis Results")
        st.success("Analysis complete!")
        with st.expander("View Analysis", expanded=True):
            if 'markdown_content' in st.session_state.current_analysis:
                st.markdown(st.session_state.current_analysis['markdown_content'])
            else:
                st.write(st.session_state.current_analysis)
    
    # Add helpful tips at the bottom
    st.header("Tips")
    st.markdown("""
    **For best results:**
    - Include complete rule syntax with all actions
    - Specify rule ID, phase, and other parameters
    - Use the example rules to test the interface
    
    **Common rule components:**
    - `SecRule`: Rule directive
    - Variables: `REQUEST_HEADERS`, `ARGS`, `FILES`, etc.
    - Operators: `@rx`, `@contains`, `@eq`, etc.
    - Actions: `deny`, `log`, `block`, `id`, `phase`, etc.
    """)

if __name__ == "__main__":
    main()