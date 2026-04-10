---
title: "Server System Warnings"
type: concept
tags: [security, logging, validation, llm-spoofing]
sources: [planning-block-validation-integration-tests]
last_updated: 2026-04-08
---

## Description
A security pattern where server-generated warnings are stored in a separate field (`_server_system_warnings`) from user-controllable warnings (`system_warnings`). This prevents LLMspoofed warnings from being injected into the response.

## Security Rationale
The LLM can only control `system_warnings` through the response. Server-side validation warnings are stored in `_server_system_warnings` which the LLM cannot influence, ensuring legitimate server warnings are preserved.

## Implementation
```python
# Server adds warnings to protected field
structured_response.debug_info["_server_system_warnings"] = ["Missing required planning block"]
```

## Connections
- Related to [[SecurityValidationTests]] for injection prevention
