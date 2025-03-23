import pytest
from app import app, PerplexityClient, check_api_key, analyze_modsec_rule

class TestRoutes:
    def test_index_route(self, client):
        # Arrange
        expected_status = 200
        
        # Act
        response = client.get('/')
        
        # Assert
        assert response.status_code == expected_status
        assert b'ModSecurity Rule Analyzer' in response.data
        
    def test_analyze_route(self, client, mocker):
        # Arrange
        mock_response = {"completion": "Analysis result"}
        mocker.patch('app.analyze_modsec_rule', return_value=mock_response)
        test_data = {'rule': 'SecRule TEST', 'prompt_template': 'Analyze: {rule}'}
        
        # Act
        response = client.post('/analyze', json=test_data)
        
        # Assert
        assert response.status_code == 200
        assert response.json == mock_response

class TestAnalyzeModsecRule:
    def test_analyze_with_perplexity(self, mocker):
        # Arrange
        api_key = "test_key"
        rule = "SecRule REQUEST_URI|ARGS \"@rx foo\" \"id:1,deny\""
        prompt = "test prompt"
        mock_response = {"completion": "Test completion"}
        
        # Mock API key check
        mocker.patch("os.getenv", return_value=api_key)
        
        # Mock LLM provider
        mock_provider = mocker.Mock()
        mock_provider.analyze.return_value = mock_response
        mocker.patch("llms.factory.LLMFactory.create", return_value=mock_provider)
        
        # Act
        result = analyze_modsec_rule(rule, prompt, provider="perplexity")
        
        # Assert
        assert result == mock_response
        mock_provider.analyze.assert_called_once()

class TestHelperFunctions:
    def test_check_api_key_present(self, mocker):
        # Arrange
        mocker.patch.dict('os.environ', {'PERPLEXITY_API_KEY': 'test_key'})
        
        # Act
        result = check_api_key()
        
        # Assert
        assert result == 'test_key'
        
    def test_check_api_key_missing(self, mocker):
        # Arrange
        mocker.patch.dict('os.environ', {}, clear=True)
        
        # Act/Assert
        with pytest.raises(ValueError):
            check_api_key()
            
    def test_analyze_modsec_rule(self, mocker):
        # Arrange
        rule = "SecRule REQUEST_URI"
        prompt_template = "Analyze this rule: {rule}"
        mock_client = mocker.Mock()
        mock_client.analyze.return_value = {"completion": "Rule analysis"}
        mocker.patch('app.PerplexityClient', return_value=mock_client)
        mocker.patch('app.check_api_key', return_value='test_key')
        
        # Act
        result = analyze_modsec_rule(rule, prompt_template)
        
        # Assert
        assert isinstance(result, dict)
        assert "completion" in result
        mock_client.analyze.assert_called_once()