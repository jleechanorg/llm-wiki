---
title: "Keyword-Only Arguments"
type: concept
tags: [python, functions, parameters]
sources: []
last_updated: 2026-04-08
---

Python function parameters that must be passed as keywords (after `*` or `*args`). The `_maybe_get_gemini_code_execution_evidence` function requires a `context` keyword-only argument.

## Syntax
```python
def func(*, required_keyword):
    pass

func(required_keyword="value")  # Valid
func("value")  # TypeError
```

## Related Pages
- [[GeminiCodeExecutionEvidenceContextParameterRegression]] — documents the bug this concept caused
