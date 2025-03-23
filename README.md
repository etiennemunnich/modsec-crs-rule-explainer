# ModSecurity Rule Analyzer

[![Python application](https://github.com/etiennemunnich/modsecurity-rule-analyzer/actions/workflows/python-app.yml/badge.svg)](https://github.com/etiennemunnich/modsecurity-rule-analyzer/actions/workflows/python-app.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Security Policy](https://img.shields.io/badge/security-policy-brightgreen.svg)](SECURITY.md)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A powerful AI-powered tool for analyzing ModSecurity rules using the Perplexity sonar-deep-research model. This tool helps security professionals understand, evaluate, and improve their WAF rules by providing comprehensive analysis and testing recommendations.

## Features

- Advanced ModSecurity rule analysis using AI (currently supporting Perplexity)
- Comprehensive security analysis including:
  - Rule purpose and objectives
  - Component-wise breakdown and security implications
  - Version compatibility analysis (ModSecurity v2/v3, CRS versions)
  - Execution phase analysis
  - RuleID significance evaluation
- Detailed security assessment covering:
  - Strengths and weaknesses analysis
  - False positive potential
  - Performance implications
  - Evasion techniques
- Test case generation with curl examples
- Docker containerized deployment for easy setup
- Both web UI and CLI interfaces

## Security Notice

This project uses API keys for various services. Never commit your API keys to the repository. Instead:

1. Copy `.env.example` to `.env`
2. Replace the placeholder values in `.env` with your actual API keys
3. The `.env` file is listed in `.gitignore` to prevent accidental commits

## Setup

### Prerequisites
- Docker and Docker Compose (for containerized deployment)
- Python 3.8+ (for local development)
- Perplexity API key

### Docker Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/modsecurity-rule-analyzer.git
   cd modsecurity-rule-analyzer
   ```

2. Configure environment:
   ```bash
   cp .env.example .env
   # Edit .env and add your PERPLEXITY_API_KEY
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
   cp .env.example .env
   # Add your PERPLEXITY_API_KEY to .env
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage

### Web Interface
1. Access the web interface at http://localhost:8501
2. Enter your ModSecurity rule in the text area
3. Click "Analyze Rule" to get detailed analysis
4. Review the comprehensive analysis output including:
   - Rule purpose and security objectives
   - Detailed component breakdown
   - Security implications and effectiveness
   - Testing recommendations
   - Additional security considerations

### CLI Usage
The tool can also be used from the command line:

```bash
# Basic usage
python cli.py "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""

# Using a custom prompt template
python cli.py --prompt-template "Analyze this ModSecurity rule focusing on potential false positives: {rule}" "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""

# Specifying the AI provider (currently supports: perplexity)
python cli.py --provider perplexity "SecRule REQUEST_HEADERS:User-Agent \"@rx malicious\" \"id:1234,phase:1,deny,log,msg:'Malicious User Agent'\""
```

Note: Make sure to set the appropriate environment variables for your chosen provider in .env file:
```bash
# For Perplexity:
perplexity_api_key=your_api_key_here
```

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
- Purpose: Detecting automated security scanning tools
- Phase analysis: Why phase 2 is appropriate
- Regular expression analysis and recommendations
- False positive scenarios and mitigation
- Testing examples with curl commands
- Version compatibility notes
- Performance impact assessment

## Testing

The analyzer generates curl test cases. Example test command:

```bash
curl -H "User-Agent: acunetix-scanner" http://your-server/
```

These test cases help verify both:
- True positive scenarios (rule should trigger)
- False positive scenarios (rule should not trigger)
- Evasion technique testing
- Performance impact assessment

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
