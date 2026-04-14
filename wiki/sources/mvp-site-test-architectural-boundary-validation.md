---
title: "test_architectural_boundary_validation.py"
type: source
tags: [test, architecture, boundary, field, validation]
date: 2025-MM-DD
source_file: raw/mvp_site_all/test_architectural_boundary_validation.py
---

## Summary
RED-GREEN tests validating field format consistency across all architectural boundaries: Frontend → main.py (API Gateway), main.py → world_logic.py (MCP Protocol), world_logic.py → Response. Tests BOTH intentional translation patterns AND potential mismatches.

## Key Claims
- Frontend sends "input" field, main.py expects "input" field
- MCP protocol uses "user_input" field in world_logic.py
- Translation layer converts between "input" (frontend) and "user_input" (MCP)
- Error/success fields ("error", "success") consistent across all boundaries
- Story entries must use "text" field (not "story") for UI compatibility
- Wrong field access results in None extraction
- Field constants defined: KEY_USER_INPUT, KEY_SUCCESS, KEY_ERROR
- Complete flow: Frontend 'input' → MCP 'user_input' → Story 'text'

## Key Connections
- Core validation for [[mvp-site-api-response-format-consistency]]
- Tests field translation between layers
- Bug fix: story entries now use "text" instead of "story"
- Cross-boundary consistency affects [[mvp-site-game-state]]

## Related Test Files
- [[mvp-site-test-api-response-format-consistency]] - response formats
- [[mvp-site-test-api-routes]] - route testing