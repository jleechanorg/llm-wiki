---
title: "Minimal Repro Ladder"
type: concept
tags: [TDD, testing, AI-agents, bug-fixing]
sources: [openclaw-workshop-notes]
last_updated: 2026-04-08
---

## Definition

A strict Test-Driven Development philosophy designed specifically for AI generation. When a bug is discovered, instead of asking the AI to fix code, the developer forces the AI to create the smallest possible test that reproduces the bug.

## The Ladder (Strict Hierarchy)

| Level | Type | Preference | Notes |
|-------|------|------------|-------|
| 1 | Unit Tests | Highest | Fastest, most deterministic |
| 2 | Backend E2E | Medium | Headless, UI-free, mocked external calls |
| 3 | Browser Tests | Lowest | Playwright/Selenium - only when UI validation needed |

## Why It Works

1. **Permanence**: Every fix hardens the codebase with automated tests
2. **Metric**: Agent has definitive, programmatic success criteria before asking for review
3. **Isolation**: Forces understanding of exact failure conditions
4. **Determinism**: Test either passes or fails - no ambiguity

## Example Application

```python
# Instead of:
"Fix the auth bug"  # Ambiguous

# Do:
"Write a test that reproduces the auth bug with these exact inputs"
# Then loop until test passes
# Human review only after test confirms fix
```

## The Minimal Repro Philosophy

> "The developer does not simply ask the AI to fix the code. Instead, they force the AI to create the smallest possible test that reproduces the bug."

## Connections

- [[TDD]] - Traditional TDD principles
- [[HarnessEngineering]] - Part of the harness
- [[ProofOfWork]] - Test as proof of work
