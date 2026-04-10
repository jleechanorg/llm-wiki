---
title: "Type Checking"
type: concept
tags: [python, type-checking, static-analysis]
sources: [mypy-configuration-worldarchitect-ai]
last_updated: 2026-04-08
---

## Definition
The practice of verifying that program values conform to expected data types at compile time (static) or runtime (dynamic). In Python, mypy provides static type checking.

## WorldArchitect.AI Usage
The project uses mypy with configurable strictness:
- warn_unreachable = True: Flags unreachable code
- disallow_untyped_defs = True: Requires type annotations in critical modules
- check_untyped_defs = True: Checks functions without annotations

## Related Concepts
- [[GradualTyping]] — mixing typed and untyped code
- [[MypyConfiguration]] — the specific config file being documented
