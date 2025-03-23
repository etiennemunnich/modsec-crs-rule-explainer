# Test Suite Documentation

This test suite follows the AAA (Arrange-Act-Assert) pattern for all test cases. The tests are organized into different classes based on the components they test:

## Test Organization

1. **TestRoutes** (`test_app.py`)
   - Tests Flask routes including index and analyze endpoints
   - Uses fixtures for Flask test client

2. **TestPerplexityClient** (`test_app.py`)
   - Tests PerplexityClient class initialization and methods
   - Uses mocking for external API calls

3. **TestHelperFunctions** (`test_app.py`)
   - Tests utility functions like check_api_key and analyze_modsec_rule
   - Uses pytest-mock for environment variables and dependencies

4. **TestCLI** (`test_cli.py`)
   - Tests command-line interface functionality
   - Tests both error cases and successful execution

## AAA Pattern Implementation

Each test follows the Arrange-Act-Assert pattern:

1. **Arrange**: Set up test data and conditions
2. **Act**: Execute the code being tested
3. **Assert**: Verify the results

Example:
```python
def test_example():
    # Arrange
    input_data = "test"
    
    # Act
    result = process(input_data)
    
    # Assert
    assert result == expected_output
```

## Test Dependencies

- pytest
- pytest-cov (for coverage reporting)
- pytest-mock (for mocking)