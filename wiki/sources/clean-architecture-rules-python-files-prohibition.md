---
title: "Critical: No New Python Files Allowed - Clean Architecture Rules"
type: source
tags: [clean-architecture, python-restriction, copilot-workflow, policy-enforcement]
source_file: "raw/clean-architecture-rules-python-files-prohibition.md"
sources: []
last_updated: 2026-04-08
---

## Summary
Document establishing strict clean architecture rules for the modular copilot system. Python is restricted to data collection only (plumbing), while Claude handles all intelligence (decision-making, response generation). New Python files require explicit "approve1234" user approval.

## Key Claims
- **Python = Data Collection Only**: Only pure data collection scripts allowed; no pattern matching, decision-making, or response generation
- **Current Allowed Files**: `commentfetch.py` (data collection), `base.py` (utilities), `utils.py` (mechanical helpers)
- **Approval Requirement**: New Python files require explicit "approve1234" user permission
- **Clean Architecture Pattern**: Python collects data → Claude reads .md files → executes actions (fixpr.md, commentreply.md, pushl.md)
- **Anti-Pattern Prevention**: Stops teams from creating Python files that violate Zero-Framework Cognition principles

## Connections
- [[Commentfetch]] — the only allowed Python data collection file
- [[CleanArchitecture]] — the concept this document enforces
- [[CommentReplyWorkflow]] — uses .md file pattern instead of Python
- [[FixprWorkflow]] — uses .md file pattern instead of Python

## Contradictions
- None detected - this policy aligns with ZFC (Zero-Framework Cognition) principles
