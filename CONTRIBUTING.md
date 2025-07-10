# Contributing to ModSecurity Rule Analyzer

First off, thank you for considering contributing to ModSecurity Rule Analyzer! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* Use a clear and descriptive title
* Describe the exact steps which reproduce the problem
* Provide specific examples to demonstrate the steps
* Describe the behavior you observed after following the steps
* Explain which behavior you expected to see instead and why
* Include screenshots if possible
* Include your environment details (OS, Python version, etc.)
* Include the ModSecurity rule that caused the issue (if applicable)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* Use a clear and descriptive title
* Provide a step-by-step description of the suggested enhancement
* Provide specific examples to demonstrate the steps
* Describe the current behavior and explain the behavior you expected to see
* Explain why this enhancement would be useful
* Include any relevant ModSecurity rule examples

### Pull Requests

* Fill in the required template
* Do not include issue numbers in the PR title
* Include screenshots and animated GIFs in your pull request whenever possible
* Follow the Python styleguides
* Include appropriate test cases
* Document new code based on the Documentation Styleguide
* End all files with a newline
* Update documentation if you've changed APIs or added new features

## Development Process

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code lints
6. Issue that pull request!

## Local Development Setup

### Prerequisites
- Python 3.8+
- Perplexity API key (for testing)

### Setup Steps
1. Clone your fork and set up the development environment:
   ```bash
   git clone https://github.com/yourusername/modsecurity-rule-analyzer.git
   cd modsecurity-rule-analyzer
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

2. Configure your environment:
   ```bash
   echo "perplexity_api_key=your_api_key_here" > .env
   ```

3. Run the application for testing:
   ```bash
   # Web interface
   streamlit run app.py
   
   # CLI testing
   python cli.py --file example_rules/sample_rule.txt
   ```

## Testing

Run the test suite using:
```bash
pytest
```

For specific test files:
```bash
pytest tests/test_app.py
pytest tests/test_cli.py
pytest tests/test_llms.py
```

## Style Guidelines

* Follow PEP 8
* Use meaningful variable names
* Write docstrings for functions and classes
* Comment your code when necessary
* Keep functions and classes focused and concise
* Use type hints where appropriate

## Project Structure

```
modsecurity-rule-analyzer/
├── app.py                 # Main Streamlit web application
├── cli.py                 # Command-line interface
├── templates/             # Prompt templates
│   └── prompt_template.py # Main analysis template
├── llms/                  # LLM provider implementations
│   ├── base.py           # Base provider interface
│   ├── perplexity.py     # Perplexity AI provider
│   └── factory.py        # Provider factory
├── tests/                 # Test suite
│   ├── test_app.py       # App functionality tests
│   ├── test_cli.py       # CLI functionality tests
│   └── test_llms.py      # LLM provider tests
├── example_rules/         # Sample ModSecurity rules
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
└── README.md             # Project documentation
```

## Adding New Features

### Adding a New LLM Provider
1. Create a new provider class in `llms/` directory
2. Inherit from `LLMProvider` base class
3. Implement the required `analyze()` method
4. Register the provider in `LLMFactory`
5. Add tests for the new provider
6. Update documentation

### Modifying the Prompt Template
1. Edit `templates/prompt_template.py`
2. Test with various rule types
3. Update documentation if template structure changes
4. Ensure backward compatibility

### Adding New CLI Options
1. Update `cli.py` argument parser
2. Add appropriate help text
3. Update tests
4. Update README.md with new usage examples

## Additional Notes

### Issue and Pull Request Labels

* `bug`: Something isn't working
* `enhancement`: New feature or request
* `documentation`: Improvements or additions to documentation
* `good first issue`: Good for newcomers
* `help wanted`: Extra attention is needed
* `question`: Further information is requested
* `cli`: Related to command-line interface
* `web-ui`: Related to Streamlit web interface
* `llm-provider`: Related to LLM provider implementations

### Commit Message Guidelines

* Use clear, descriptive commit messages
* Start with a verb (Add, Fix, Update, Remove, etc.)
* Keep the first line under 50 characters
* Add more details in the body if needed

Example:
```
Add file-based rule analysis support

- Add --file/-f option to CLI
- Support reading rules from text files
- Add error handling for file operations
- Update documentation with new usage examples
```