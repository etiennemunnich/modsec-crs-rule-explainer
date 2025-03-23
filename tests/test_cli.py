import pytest
import sys
from cli import main

class TestCLI:
    def test_cli_execution_no_args(self, capsys):
        # Arrange
        sys.argv = ['cli.py']
        expected_result = 1
        
        # Act
        result = main()
        captured = capsys.readouterr()
        
        # Assert
        assert result == expected_result
        assert "Usage:" in captured.out
        
    def test_cli_execution_with_rule(self, mocker, capsys):
        # Arrange
        test_rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
        sys.argv = ['cli.py', test_rule]
        mock_check_api_key = mocker.patch('cli.check_api_key')
        mock_check_api_key.return_value = "test_api_key"
        mock_analyze = mocker.patch('cli.analyze_modsec_rule')
        mock_analyze.return_value = {"markdown_content": "Test analysis"}
        
        # Act
        result = main()
        captured = capsys.readouterr()
        
        # Assert
        assert result == 0
        assert mock_analyze.called
        mock_analyze.assert_called_with(test_rule, 
            "Please analyze this ModSecurity rule and explain what it does, including any potential issues or improvements: {rule}",
            provider="perplexity")
        assert "Test analysis" in captured.out

    def test_cli_execution_with_custom_template(self, mocker, capsys):
        # Arrange
        test_rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
        custom_template = "Custom template: {rule}"
        sys.argv = ['cli.py', '--prompt-template', custom_template, test_rule]
        mock_check_api_key = mocker.patch('cli.check_api_key')
        mock_check_api_key.return_value = "test_api_key"
        mock_analyze = mocker.patch('cli.analyze_modsec_rule')
        mock_analyze.return_value = {"markdown_content": "Test analysis"}
        
        # Act
        result = main()
        
        # Assert
        assert result == 0
        mock_analyze.assert_called_with(test_rule, custom_template, provider="perplexity")

    def test_cli_execution_with_custom_provider(self, mocker, capsys):
        # Arrange
        test_rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
        provider = "perplexity"
        sys.argv = ['cli.py', '--provider', provider, test_rule]
        mock_check_api_key = mocker.patch('cli.check_api_key')
        mock_check_api_key.return_value = "test_api_key"
        mock_analyze = mocker.patch('cli.analyze_modsec_rule')
        mock_analyze.return_value = {"markdown_content": "Test analysis"}
        
        # Act
        result = main()
        
        # Assert
        assert result == 0
        mock_analyze.assert_called_with(test_rule, 
            "Please analyze this ModSecurity rule and explain what it does, including any potential issues or improvements: {rule}",
            provider=provider)

    def test_cli_execution_missing_api_key(self, mocker, capsys):
        # Arrange
        test_rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
        sys.argv = ['cli.py', test_rule]
        mock_check_api_key = mocker.patch('cli.check_api_key')
        mock_check_api_key.return_value = None
        
        # Act
        result = main()
        captured = capsys.readouterr()
        
        # Assert
        assert result == 1
        assert "Error: perplexity_api_key environment variable is not set" in captured.out