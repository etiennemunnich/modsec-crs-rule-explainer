import pytest
from unittest.mock import patch, Mock
import os
from app import check_api_key, analyze_modsec_rule

# Test cases for the check_api_key function
def test_check_api_key_present(monkeypatch):
    """
    Test that check_api_key returns the key when the environment variable is set.
    """
    monkeypatch.setenv("perplexity_api_key", "test_key_123")
    assert check_api_key("perplexity") == "test_key_123"

def test_check_api_key_missing(monkeypatch):
    """
    Test that check_api_key raises ValueError when the environment variable is not set.
    """
    monkeypatch.delenv("perplexity_api_key", raising=False)
    with pytest.raises(ValueError, match="perplexity_api_key environment variable not found"):
        check_api_key("perplexity")

def test_check_api_key_unknown_provider():
    """
    Test that check_api_key raises ValueError for an unknown provider.
    """
    with pytest.raises(ValueError, match="Unknown provider: unknown_provider"):
        check_api_key("unknown_provider")

# Test cases for the analyze_modsec_rule function
@patch('app.check_api_key')
@patch('app.get_llm_client')
def test_analyze_modsec_rule_success(mock_get_llm_client, mock_check_api_key):
    """
    Test a successful analysis of a ModSecurity rule.
    """
        # Arrange
    mock_check_api_key.return_value = "fake_api_key"
    
    mock_llm_client = Mock()
    mock_llm_client.analyze.return_value = {"markdown_content": "Detailed analysis"}
    mock_get_llm_client.return_value = mock_llm_client
    
    rule = "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\""
    prompt_template = "Analyze this: {rule}"
        
        # Act
    result = analyze_modsec_rule(rule, prompt_template, provider="perplexity")
        
        # Assert
    mock_check_api_key.assert_called_once_with("perplexity")
    mock_get_llm_client.assert_called_once_with("fake_api_key", "perplexity")
    
    expected_prompt = prompt_template.format(rule=rule)
    mock_llm_client.analyze.assert_called_once_with(expected_prompt)

    assert result == {"markdown_content": "Detailed analysis"}

@patch('app.check_api_key', side_effect=ValueError("API Key Not Found"))
def test_analyze_modsec_rule_api_key_error(mock_check_api_key):
    """
    Test that analyze_modsec_rule raises an exception if the API key is missing.
    """
        # Arrange
    rule = "SecRule ARGS:test"
    prompt_template = "Template: {rule}"

    # Act & Assert
    with pytest.raises(ValueError, match="API Key Not Found"):
        analyze_modsec_rule(rule, prompt_template)
    
    mock_check_api_key.assert_called_once_with("perplexity")

@patch('app.check_api_key')
@patch('app.get_llm_client')
def test_analyze_modsec_rule_llm_failure(mock_get_llm_client, mock_check_api_key):
    """
    Test how analyze_modsec_rule handles an exception from the LLM client.
    """
        # Arrange
    mock_check_api_key.return_value = "fake_api_key"
    
    mock_llm_client = Mock()
    mock_llm_client.analyze.side_effect = RuntimeError("LLM API Error")
    mock_get_llm_client.return_value = mock_llm_client

    rule = "SecRule SOME_VAR"
    prompt_template = "Analyze: {rule}"

    # Act & Assert
    with pytest.raises(RuntimeError, match="LLM API Error"):
        analyze_modsec_rule(rule, prompt_template)