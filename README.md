# ModSecurity Rule Analyzer

[![Python application](https://github.com/yourusername/modsecurity-rule-analyzer/actions/workflows/python-app.yml/badge.svg)](https://github.com/yourusername/modsecurity-rule-analyzer/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Policy](https://img.shields.io/badge/security-policy-brightgreen.svg)](SECURITY.md)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful AI-powered tool for analyzing ModSecurity rules using the Perplexity sonar-reasoning-pro model. This tool helps security professionals understand, evaluate, and improve their WAF rules by providing comprehensive analysis and testing recommendations.

NOTE: This uses a reasoning model to provide part of the output and should be validated as AI may not provide full contextual answers nor provide correct answers. So please validate all output.  I am working on another approach using local LLMs with RAG/CAG and/or a ML model specifically for this purpose.

DISCLAIMER: Please validatate this project and it's outputs for your use-case and do not use in production until fully tested for your-use case. Provided as is and use at your own risk.

## Quick Start

### Run the Web Interface
```bash
# Install dependencies
pip install -r requirements.txt

# Set up your API key
echo "perplexity_api_key=your_api_key_here" > .env

# Start the web interface
streamlit run app.py
```

Then open your browser to http://localhost:8501

### Run from Command Line
```bash
# Analyze a rule directly
python cli.py "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""

# Analyze a rule from file
python cli.py --file example_rules/sample_rule.txt
```

## Features

- **Advanced ModSecurity rule analysis** using AI (currently supporting Perplexity)
- **Comprehensive security analysis** including:
  - Rule purpose and objectives
  - Component-wise breakdown and security implications
  - Version compatibility analysis (ModSecurity v2/v3, CRS versions)
  - Execution phase analysis
  - RuleID significance evaluation
- **Detailed security assessment** covering:
  - Strengths and weaknesses analysis
  - False positive potential
  - Performance implications
  - Evasion techniques
- **Test case generation** with curl examples
- **Docker containerized deployment** for easy setup
- **Both web UI and CLI interfaces**
- **File-based rule analysis** support
- **Customizable prompt templates**

## Security Notice

This project uses API keys for various services. Never commit your API keys to the repository. Instead:

1. Copy `.env.example` to `.env` 
2. Replace the placeholder values in `.env` with your actual API keys


## Setup

### Prerequisites
- Docker and Docker Compose (for containerized deployment)
- Python 3.8+ (for local development)
- Perplexity API key
- Ollama (for local AI analysis with Gemma3:latest)

### Docker Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modsecurity-rule-analyzer.git
   cd modsecurity-rule-analyzer
   ```

2. Configure environment:
   ```bash
   # Create .env file with your API key
   echo "perplexity_api_key=your_api_key_here" > .env
   ```

3. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the web interface at http://localhost:8501

### Local Development Setup
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```bash
   # Create .env file with your API key
   echo "perplexity_api_key=your_api_key_here" > .env
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

### Ollama Setup (for Local AI Analysis)

To use the local Ollama provider with Gemma3:latest:

1. **Install Ollama:**
   ```bash
   # macOS and Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Windows
   # Download from https://ollama.ai/download
   ```

2. **Pull the Gemma3:latest model:**
   ```bash
   ollama pull gemma3:latest
   ```

3. **Start Ollama service:**
   ```bash
   ollama serve
   ```

4. **Test the model:**
   ```bash
   ollama run gemma3:latest "Hello, how are you?"
   ```

5. **Use in the application:**
   - Select "ollama" as the AI provider in the web interface
   - Or use `--provider ollama` in the CLI
   - No API key required for Ollama (runs locally)

## Usage

### Web Interface
The web interface provides an intuitive way to analyze ModSecurity rules with AI assistance.

#### Getting Started
1. **Start the application:**
   ```bash
   streamlit run app.py
   ```

2. **Access the interface:**
   - Open your web browser
   - Navigate to http://localhost:8501
   - You'll see the redesigned ModSecurity Rule Analyzer interface.

#### How to Use the Web Interface

**Step 1: Enter or Load a ModSecurity Rule**
- **Option A: Paste your rule**
  - Click in the large text area labeled "Enter your ModSecurity rule".
  - Paste your complete ModSecurity rule.
- **Option B: Use an example rule**
  - Look at the sidebar on the left.
  - Under "Example Rules", select one from the dropdown (e.g., Scanner Detection, SQL Injection).
  - The rule will automatically populate the main input area.
- **Option C: Load from history**
  - In the sidebar, under "Analysis History", click on a previously analyzed rule.
  - The rule and its corresponding analysis will be loaded into the main view.

**Step 2: Analyze the Rule**
- Click the blue "Analyze Rule" button.
- Wait for the analysis to complete (you'll see a spinner).
- The detailed analysis will appear below the input area.

**Step 3: Review the Results**
- The analysis is displayed in an expandable section titled "Analysis Results".
- The output includes a rule overview, technical breakdown, security impact, test cases, and more.

**Step 4: Clear the Input**
- Click the "Clear Input" button to reset the text area and the analysis results.

#### Interface Features

**Sidebar (on the left):**
- **LLM Provider**: Select the AI provider (supports Perplexity, OpenAI, X.com, Google, and Ollama).
- **Quick Start Guide**: A brief guide on how to use the app.
- **Example Rules**: A dropdown to load pre-built rules for quick testing.
- **Analysis History**: A list of your past analyses. Click any entry to reload the rule and its results.

**Main Content Area:**
- **Rule Input Area**: A large text area for pasting or loading rules.
- **Analyze and Clear Buttons**: Primary actions for the application.
- **Analysis Results**: An expandable section where the detailed breakdown from the AI is displayed.
- **Tips Section**: Helpful information and best practices for writing ModSecurity rules.

#### Troubleshooting

**Common Issues:**
- **"Please enter a ModSecurity rule"**: Make sure you've pasted a rule in the text area before clicking "Analyze Rule".
- **API Key Error**: Ensure your `perplexity_api_key` is set correctly in your `.env` file.
- **Analysis Fails**: Check that your rule follows proper ModSecurity syntax.
- **Page Not Loading**: Make sure the Streamlit server is running correctly.

**Getting Help:**
- Use the example rules to test the interface
- Check the tips section for syntax guidance
- Review the analysis history for similar rules

### CLI Usage
The tool can be used from the command line in several ways:

```bash
# Basic usage with inline rule (default: Perplexity)
python cli.py "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""

# Using a rule from a file
python cli.py --file example_rules/sample_rule.txt
# or using the short form
python cli.py -f example_rules/sample_rule.txt

# Using a custom prompt template
python cli.py --prompt-template "Analyze this ModSecurity rule focusing on potential false positives: {rule}" "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""

# Combining file input with custom template
python cli.py --file example_rules/sample_rule.txt --prompt-template "Analyze this ModSecurity rule focusing on potential false positives: {rule}"

# Specifying the AI provider (Perplexity, OpenAI, X.com, Google, Ollama)
python cli.py --provider perplexity "SecRule ..."
python cli.py --provider openai "SecRule ..."
python cli.py --provider xcom "SecRule ..."
python cli.py --provider google "SecRule ..."
python cli.py --provider ollama "SecRule ..."
```

### Environment Configuration
Set the appropriate environment variables in your `.env` file for the providers you want to use:
```bash
# For Perplexity:
perplexity_api_key=your_api_key_here
# For OpenAI:
openai_api_key=your_openai_api_key_here
# For X.com:
xcom_api_key=your_xcom_api_key_here
# For Google:
google_api_key=your_google_api_key_here
# For Ollama (no API key required - runs locally):
# No environment variable needed
```

### CLI Options
The CLI supports the following options:
- `rule`: The ModSecurity rule to analyze (required if not using --file)
- `--file`, `-f`: Path to a file containing the ModSecurity rule to analyze (required if not providing rule directly)
- `--prompt-template`: Custom prompt template (optional)
- `--provider`: AI provider to use (default: perplexity)

### Analysis Output
The tool provides a detailed analysis following our comprehensive template structure, including:
- **Rule Overview**: Purpose, TTPs, OWASP Top 10/API Top 10, CVEs, CWEs, and risk mitigation
- **Technical Analysis**: Rule ID, type, variables, operators, actions, and phase
- **Security Impact**: CRS rule ID, attack types, impact assessment, and TTPs mitigated
- **Effectiveness and False Positives**: Detection effectiveness, common false positives, and improvement suggestions
- **Version Comparison**: ModSecurity v2/v3 differences and CRS version compatibility
- **Potential Improvements**: Rule enhancements, additional conditions, and regex improvements
- **Test Cases**: True positive and false positive test scenarios with curl commands
- **Summary**: Comprehensive rule summary with relevant documentation links

## Example Analysis

Here's an example of analyzing a scanner detection rule:

```apache
SecRule REQUEST_HEADERS:User-Agent "@rx (?:acunetix|analyze|audit|black|scan|nikto)" \
    "id:949110,\
    phase:2,\
    block,\
    t:none,t:lowercase,\
    log,\
    msg:'Scanner Detection - Security Scanner Identified',\
    logdata:'%{MATCHED_VAR}',\
    tag:'scanner',\
    severity:'CRITICAL',\
    ver:'OWASP_CRS/3.3.2',\
    setvar:'tx.anomaly_score_pl1=+%{tx.critical_anomaly_score}'"
```

The analyzer will provide detailed insights including:
- **Purpose**: Detecting automated security scanning tools
- **Phase Analysis**: Why phase 2 is appropriate for request body processing
- **Regular Expression Analysis**: Pattern effectiveness and recommendations
- **False Positive Scenarios**: Common legitimate use cases that might trigger the rule
- **Testing Examples**: Curl commands for both true and false positive scenarios
- **Version Compatibility**: Notes on ModSecurity v2/v3 and CRS version differences
- **Performance Impact**: Assessment of rule performance implications

## Testing

The analyzer generates comprehensive test cases. Example test commands:

```bash
# True positive test
curl -H "User-Agent: acunetix-scanner" http://your-server/

# False positive test
curl -H "User-Agent: Mozilla/5.0 (compatible; legitimate-bot)" http://your-server/
```

These test cases help verify:
- **True Positive Scenarios**: Rules trigger correctly for malicious traffic
- **False Positive Scenarios**: Rules don't trigger for legitimate traffic
- **Evasion Technique Testing**: Detection of bypass attempts
- **Performance Impact Assessment**: Rule efficiency evaluation

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
├── example_rules/         # Sample ModSecurity rules
├── requirements.txt       # Python dependencies
├── docker-compose.yml     # Docker configuration
└── README.md             # This file
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

For security issues, please see [SECURITY.md](SECURITY.md) for reporting guidelines.