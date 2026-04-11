---
title: "Implementation vs Orchestration Decision Framework"
type: source
tags: [worldarchitect-ai, code-quality, architecture, anti-patterns, orchestration]
sources: []
date: 2025-08-21
source_file: raw/implementation-decision-framework.md
last_updated: 2026-04-07
---

## Summary
A systematic framework that prevents fake code creation by requiring developers to answer "Can I implement this function fully right now?" before implementing. Provides clear decision criteria for when to implement directly, use orchestration of existing commands, or avoid creating placeholder code.

## Key Claims

- **Pre-Implementation Decision Gate**: Mandatory question "Can I implement this function fully right now?" before any implementation work begins
- **Implement Directly Criteria**: All dependencies available, clear well-defined functionality, can write working code immediately, no existing command handles this need
- **Use Orchestration Criteria**: Existing command provides functionality (e.g., `/commentfetch`), need to combine multiple capabilities, can delegate to proven implementations
- **Never Create Placeholder**: Missing dependencies or infrastructure, unclear requirements, would need fake/simulation code, planning to "implement later"
- **Red Flags**: TODO comments in function bodies, placeholder return values, "implement later" comments, hardcoded None returns with "fallback" comments

## Key Quotes

> "MANDATORY QUESTION: Can I implement this function fully right now?"

> "Instead of Creating Fake Code: Use orchestration - call existing command"

## Connections

- Related to [[Schema Test Centralization]] — testing framework that ensures real code works
- Related to [[GitHub Production Workflow Fix]] — prevents misconfigured deployments from fake implementations

## Contradictions

- None identified — this framework is complementary to existing development practices

## Patterns

### Orchestration Pattern 1: Command Composition
```markdown
# gstatus.md - Orchestrates existing commands
/commentfetch  # Use existing GitHub integration
python3 .claude/commands/gstatus.py  # Handle display logic
```

### Orchestration Pattern 2: Utility Function Reuse
```python
from existing_module import validated_api_call
result = validated_api_call("github", params)
```

### Orchestration Pattern 3: Incremental Building
```python
def complex_operation(data):
    validated = validate_input(data)  # Working function
    processed = transform_data(validated)  # Working function  
    return format_output(processed)  # Working function
```
