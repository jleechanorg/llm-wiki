# Remove mock-mode path from MCP/UI smoke testing

**Type:** task
**Priority:** 1
**Status:** open
**Labels:** testing, smoke, evidence, reliability

## Summary

The MCP and UI test suites were still carrying mock-mode control paths (especially in `testing_mcp/test_smoke.py`, `testing_mcp/lib/base_test.py`, and `testing_mcp/lib/evidence_utils.py`) via `MCP_TEST_MODE`/conditional mock allowances. These paths relaxed validation and changed behavior depending on mock service mode.

## Decision

Per request, this branch now enforces real-service behavior for MCP/UI validation paths:
- Remove MCP_TEST_MODE-driven mock switching in smoke startup and server restart flows.
- Remove mock-mode conditional evidence checks in base/evidence helpers.
- Keep campaign export behavior tied to local server provenance only.
- Remove mock mode mentions from smoke mode manifest (`testing_mcp/lib/smoke_test_modes.py` + `testing_mcp/smoke_test_modes.json`).
- Clarify no-mock policy in `AGENTS.md` and `CLAUDE.md`.

## Files changed

- `testing_mcp/test_smoke.py`
- `testing_mcp/lib/base_test.py`
- `testing_mcp/lib/evidence_utils.py`
- `testing_mcp/lib/server_utils.py`
- `testing_mcp/lib/smoke_test_modes.py`
- `testing_mcp/smoke_test_modes.json`
- `AGENTS.md`
- `CLAUDE.md`

## Validation impact

These changes remove conditional relaxations that previously skipped invariant checks when mock mode was enabled, making MCP/UI smoke runs stricter and aligned to real-service evidence requirements.
