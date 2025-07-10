#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv
from app import analyze_modsec_rule, check_api_key
from templates.prompt_template import PROMPT_TEMPLATE

def read_rule_from_file(file_path: str) -> str:
    """Read a rule from a file.
    
    Args:
        file_path: Path to the file containing the rule
        
    Returns:
        The rule as a string
    """
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f"Error reading rule file: {str(e)}")
        return None

def main():
    parser = argparse.ArgumentParser(description='Analyze ModSecurity rules using AI')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('rule', nargs='?', help='The ModSecurity rule to analyze')
    group.add_argument('--file', '-f', help='Path to a file containing the ModSecurity rule to analyze')
    parser.add_argument('--prompt-template', 
                       help='Custom prompt template (optional)',
                       default=None)  # We'll set the default after loading the template
    parser.add_argument('--provider',
                       help='AI provider to use (default: perplexity)',
                       default="perplexity",
                       choices=['perplexity', 'openai', 'xcom', 'google', 'ollama'])
    args = parser.parse_args()
    
    # Load environment variables and check API key
    load_dotenv()
    api_key = check_api_key(args.provider)
    if not api_key:
        print(f"Error: {args.provider}_api_key environment variable is not set")
        return 1
    
    # Set default template if none provided
    if args.prompt_template is None:
        args.prompt_template = PROMPT_TEMPLATE
    
    # Get the rule either from command line or file
    rule = args.rule
    if args.file:
        rule = read_rule_from_file(args.file)
        if rule is None:
            return 1
    
    # Analyze the rule
    try:
        result = analyze_modsec_rule(rule, args.prompt_template, provider=args.provider)
        print("\nAnalysis Result:")
        print("-" * 40)
        print(f"Rule: {rule}")
        print("-" * 40)
        print(f"Analysis: {result['markdown_content']}")
        return 0
    except Exception as e:
        print(f"Error analyzing rule: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())