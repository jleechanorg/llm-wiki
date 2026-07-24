---
name: gate8-requires-real-smoke-mode
description: Green Gate Gate-8 requires real-mode smoke tests; default workflow_dispatch uses mock mode which fails Gate-8
type: feedback
bead: none
---

When dispatching MCP smoke tests for Gate-8 satisfaction, ALWAYS pass `-f test_mode=real`:

```bash
gh workflow run mcp-smoke-tests.yml \
  --ref <branch> \
  -f pr_number=<N> \
  -f test_mode=real
```

**Why:** `mcp-smoke-tests.yml` defaults `test_mode` to `mock`. Gate-8 in `green-gate.yml` explicitly checks for `<!-- mcp-smoke-mode: real -->` in the smoke comment. A mock run posts `<!-- mcp-smoke-mode: mock -->` and triggers the gate failure message: "GATE-8 FAIL: exact mcp-smoke-tests succeeded in MOCK mode — a mock smoke does not satisfy the gate; run /smoke for real-service coverage."

**How to apply:** Any time you dispatch smoke tests to satisfy Gate-8, include `-f test_mode=real`. The `/smoke` slash command handles this automatically. Manual `gh workflow run` does not.

**Real mode timing:** ~24 min total (3 providers × ~8 min each). Plan accordingly when estimating time to Gate-8 satisfaction.

**References:**
- `green-gate.yml` Gate-8 check: looks for `<!-- mcp-smoke-mode: real -->` in PR comments for current HEAD SHA
- `mcp-smoke-tests.yml` line 27-34: `test_mode` input defaults to `mock`
- Incident: PR #7802 session, smoke runs `28009127701` (real, dispatched correctly after discovering the issue)
