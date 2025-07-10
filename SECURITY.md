# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ----------------- |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of ModSecurity Rule Analyzer seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to [security@example.com](mailto:security@example.com) (replace with actual security contact).

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the requested information listed below (as much as you can provide) to help us better understand the nature and scope of the possible issue:

* Type of issue (e.g. buffer overflow, SQL injection, cross-site scripting, API key exposure, etc.)
* Full paths of source file(s) related to the manifestation of the issue
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit the issue
* For API-related issues, include the specific API endpoint and request/response details

This information will help us triage your report more quickly.

## Security Considerations for This Project

### API Key Security
- Never commit API keys to the repository
- Use environment variables for sensitive configuration
- The `.env` file is gitignored to prevent accidental commits
- Rotate API keys regularly

### Input Validation
- All ModSecurity rules are validated before processing
- File inputs are sanitized to prevent path traversal attacks
- Prompt templates are validated to prevent injection attacks

### Output Sanitization
- Analysis outputs are sanitized to prevent XSS in web interface
- Error messages are generic to avoid information disclosure

## Preferred Languages

We prefer all communications to be in English.

## Policy

We follow the principle of [Responsible Disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).