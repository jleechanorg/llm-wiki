---
title: "Input Field Translation"
type: concept
tags: [architecture, translation-layer, api-design]
sources: ["input-field-translation-validation-tests"]
last_updated: 2026-04-08
---

The architectural pattern of translating field names between different protocol layers. In this codebase, the translation layer converts frontend requests (using `input` field) to MCP protocol (using `user_input` field) before forwarding to [[world_logic.py]].

## Translation Chain
1. **Frontend** → sends `{"input": "..."}`
2. **main.py** → receives via `KEY_USER_INPUT = "input"`, translates to `"user_input"`
3. **MCP Protocol** → carries `"user_input"` field
4. **world_logic.py** → receives via `KEY_USER_INPUT = "user_input"`

## Compatibility Layer
main.py supports both:
- `input` — preferred (frontend standard)
- `user_input` — legacy fallback

Priority: `input` wins when both present.

## Related Tests
- [[Input Field Translation Validation Tests]] — RED→GREEN tests for field translation
