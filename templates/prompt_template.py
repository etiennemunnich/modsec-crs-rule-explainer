PROMPT_TEMPLATE = """
Analyze the following ModSecurity/OWASP CRS rule and provide a detailed analysis including:

Rule: {rule}

Please provide your analysis in the following markdown format:

## Rule Overview
[150 words or less: Provide a brief overview of what the rule does, include TTPs and what risks it mitigates, etc.]

## Technical Analysis
Table:
- Rule ID: [Rule ID]
- Rule Type: [SecRule, SecAction, etc.]
- Variables: [List variables being examined]
- Operators: [List operators used]
- Actions: [List actions taken]
- Phase: [Which phase the rule executes in]

## Security Impact
Table format:
- CRS rule ID: [CRS rule ID] or ModSecurity rule ID: [ModSecurity rule ID
- Attack Type: [What type of attack this rule protects against]
- Impact: [What impact does this rule have on security]
- TTPs: [TTPs mitigated by this rule]

## Effectiveness and False Postives
- How effective is this rule at detecting common attacks? (CVEs, OWASP Top 10, CRS version etc.)
- Are there any common false positives associated with this rule?
- How could this rule be improved to reduce false positives?

## Comparison of versions
- Compare this rule to other similar rules in terms of effectiveness and false positives
- Compare ModeSecurity Versions: Are there any differences in how this rule is implemented in different versions of ModSecurity?
- Compare Core Rule Set Versions: Are there any differences in how this rule is implemented in different versions of the Core Rule Set?

## Potential Improvements and Additional Conditions
- Are there any potential improvements to this rule?
- Are there any additional conditions that could be added to improve detection?
- Regex improvements: Are there any regex improvements that could be made to this rule?

## Suggest improvements
- provide 1-3 suggestions for improving the rule, including any additional conditions or changes to existing
- provide a brief explanation of why you think these changes would be beneficial

## Test case

```bash
[Add curl test here]
```



## Summary
[300 words or less: Summary of rule and any other relevant information or considerations]
"""