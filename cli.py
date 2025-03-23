#!/usr/bin/env python3
import argparse
import os
from dotenv import load_dotenv
from app import analyze_modsec_rule, check_api_key

def main():
    parser = argparse.ArgumentParser(description='Analyze ModSecurity rules using AI')
    parser.add_argument('rule', help='The ModSecurity rule to analyze')
    parser.add_argument('--prompt-template', 
                       help='Custom prompt template (optional)',
                       default="Please analyze this ModSecurity rule and explain what it does, including any potential issues or improvements: {rule}")
    parser.add_argument('--provider',
                       help='AI provider to use (default: perplexity)',
                       default="perplexity",
                       choices=['perplexity'])
    args = parser.parse_args()
    
    # Load environment variables and check API key
    load_dotenv()
    api_key = check_api_key(args.provider)
    if not api_key:
        print(f"Error: {args.provider}_api_key environment variable is not set")
        return 1
    
    # Analyze the rule
    try:
        result = analyze_modsec_rule(args.rule, args.prompt_template, provider=args.provider)
        print("\nAnalysis Result:")
        print("-" * 40)
        print(f"Rule: {args.rule}")
        print("-" * 40)
        print(f"Analysis: {result['markdown_content']}")
        return 0
    except Exception as e:
        print(f"Error analyzing rule: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())