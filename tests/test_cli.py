import subprocess
import sys
import os
import pytest

CLI_PATH = os.path.join(os.path.dirname(__file__), '..', 'cli.py')

@pytest.mark.parametrize("provider,env_var,expected_tag", [
    ("perplexity", "perplexity_api_key", "[Perplexity"),
    ("openai", "openai_api_key", "[OpenAI"),
    ("xcom", "xcom_api_key", "[X.com"),
    ("google", "google_api_key", "[Google"),
])
def test_cli_provider_output(tmp_path, provider, env_var, expected_tag):
    rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
    env = os.environ.copy()
    env[env_var] = "dummy_key"
    cmd = [sys.executable, CLI_PATH, '--provider', provider, rule]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert expected_tag in result.stdout

def test_cli_missing_api_key():
    rule = 'SecRule REQUEST_HEADERS:User-Agent "@rx malicious"'
    env = os.environ.copy()
    # Remove all possible API keys
    for var in ["perplexity_api_key", "openai_api_key", "xcom_api_key", "google_api_key"]:
        env.pop(var, None)
    cmd = [sys.executable, CLI_PATH, '--provider', 'openai', rule]
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    assert result.returncode == 1
    assert "openai_api_key environment variable is not found" in result.stdout or "openai_api_key environment variable not found" in result.stdout