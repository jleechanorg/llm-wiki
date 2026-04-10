---
title: "Gradual Typing"
type: concept
tags: [python, typing, strategy]
sources: [python-typing-guide]
last_updated: 2026-04-08
---

Gradual typing is WorldArchitect.AI's approach to adding types incrementally: start with critical modules, add types to new code immediately, type existing code when modifying, and increase strictness over time.

## Implementation Strategy
1. Start with critical modules (services, main application)
2. Add types to new code immediately
3. Type existing code when modifying
4. Increase strictness over time

## Related
- [[PythonTypingGuide]] — full guide
- [[TypeHints]] — PEP 484 standard
- [[mypy]] — type checker
