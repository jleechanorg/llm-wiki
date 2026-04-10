---
title: "world_logic.py"
type: entity
tags: [file, python, mcp, protocol-handler]
sources: ["input-field-translation-validation-tests"]
last_updated: 2026-04-08
---

MCP protocol handler that receives translated requests from [[main.py]]. Uses `KEY_USER_INPUT = "user_input"` to extract user input from MCP-formatted requests. Part of the backend stack that processes game logic and AI responses.

## Key Responsibilities
- Receive MCP-formatted requests with `user_input` field
- Extract user input using `KEY_USER_INPUT = "user_input"`
- Process game interactions and return AI responses
- Handle multiple interaction modes (character, god, etc.)

## Related Tests
- [[Input Field Translation Validation Tests]] — validates field extraction chain
