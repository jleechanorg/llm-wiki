---
title: "SWE-bench"
type: concept
tags: [swe-bench, benchmark, llm, software-engineering]
last_updated: 2026-04-14
---

## Summary

SWE-bench is a benchmark for evaluating LLMs on real-world software engineering tasks. It takes GitHub issues from popular open-source repositories and tests whether an LLM can successfully resolve them.

## How It Works

1. **Issue selection** — Real GitHub issues selected from Python projects (Django, Flask, etc.)
2. **Reference resolution** — Ground truth commits provide the expected fix
3. **Test generation** — Unit tests created from the issue description
4. **Evaluation** — LLM produces a patch; patch applied and tested against the test suite

## Key Metrics

- **Pass@K** — Rate of successful resolution within top K attempts
- **Resolution rate** — Percentage of issues fully resolved
- **Patch quality** — Exact match vs. functional equivalence

## Evaluation Harness

```python
# Simplified SWE-bench evaluation
result = evaluate(
    model="claude-sonnet-4",
    dataset="swe-bench-lite",
    instance=issue_instance,
    timeout=1800  # 30 min per instance
)
```

## Connections

- [[CanonicalCodeScorer]] — Code scoring systems
- [[AgentArchitecture]] — Agent design for coding tasks
- [[AdversarialTesting]] — Testing LLM limits
