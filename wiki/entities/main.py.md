---
title: "main.py"
type: entity
tags: [file, python, flask, translation-layer]
sources: ["input-field-translation-validation-tests"]
last_updated: 2026-04-08
---

Flask application entry point that handles HTTP request translation between frontend and MCP protocol. Acts as the translation layer that converts frontend field names (`input`) to MCP field names (`user_input`) before forwarding to [[world_logic.py]].

## Key Responsibilities
- Extract user input from frontend requests via `data.get("input")`
- Translate to MCP protocol format using `KEY_USER_INPUT = "input"`
- Support legacy payloads with `user_input` key fallback
- Forward translated requests to MCP handler

## Related Tests
- [[Input Field Translation Validation Tests]] — validates field translation chain
