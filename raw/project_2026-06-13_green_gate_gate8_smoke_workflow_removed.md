---
name: project-2026-06-13-green-gate-gate8-smoke-workflow-removed
description: mcp-smoke-tests.yml removed in
metadata: 
  node_type: memory
  type: project
  originSessionId: 33b6218a-1fc0-42b9-b4f8-1814474904eb
---

# Green Gate Gate 8 is deadlocked for any PR touching mvp_site/**/*.py

**Date:** 2026-06-13
**Symptom:** PRs with individual checks all SUCCESS fail Green Gate with "GATE-8 FAIL: timed out waiting for mcp-smoke-tests for SHA <sha>" (e.g. #7518 run 27462268175).

**Root cause:** `mcp-smoke-tests.yml` was REMOVED from origin/main in commit b26a5eb1e9 (PR #7517) on 2026-06-13. The commit message: *"Originally added in PR #1998... Manually disabled via gh api on 2026-06-13 (state: disabled_manually) because the 4 trigger types (issue_comment, workflow_dispatch, workflow_run, pull_request) were driving re-queue loops in the GitHub Actions self-hosted runner pool after merges."* But `green-gate.yml` Gate 8 still runs its `gh run list --workflow mcp-smoke-tests.yml` poll loop 45 times and times out.

**Path filter that triggers Gate 8** (green-gate.yml ~line 552):
```bash
if echo "$CHANGED" | grep -qE '^mvp_site/prompts/|^mvp_site/.+\.py$'; then
  SMOKE_REQUIRED=true
fi
```
This regex matches:
- `mvp_site/prompts/...` (prompts)
- `mvp_site/**/*.py` — including `mvp_site/tests/test_*.py`, `mvp_site/world_logic.py`, `mvp_site/llm_service.py`, `mvp_site/llm_providers/*.py`, etc.

So **every** production PR that touches a `.py` file under `mvp_site/` is deadlocked.

**Affected in-flight PRs (2026-06-13):**
- [#7518](https://github.com/jleechanorg/worldarchitect.ai/pull/7518) (ratchet, test-only at mvp_site/tests/test_output_token_budget_regression.py)
- [#7480](https://github.com/jleechanorg/worldarchitect.ai/pull/7480) (no-second-llm, 197+/-1453 across world_logic.py + llm_service.py + provider_utils.py)
- [#7436](https://github.com/jleechanorg/worldarchitect.ai/issues/7436) streaming-request-json (no PR yet, will hit same gate)

**How to unblock (proposed 5-10 line diff in green-gate.yml):**
```bash
# At the top of the gate-8 step, before SMOKE_REQUIRED computation:
WORKFLOW_EXISTS=$(gh api repos/${{ github.repository }}/contents/.github/workflows/mcp-smoke-tests.yml --jq '.name' 2>/dev/null || echo "")
if [ -z "$WORKFLOW_EXISTS" ]; then
  echo "GATE-8: mcp-smoke-tests workflow not present in repo — skipping (see #7517)"
  echo "smoke_gate=PASS" >> "$GITHUB_OUTPUT"
  exit 0
fi
```

**Alternative:** restore the mcp-smoke-tests workflow — but #7517 was removed for a real reason (re-queue loops), so the gating should detect the missing workflow, not bring the workflow back.

**Status (2026-06-13T~10:25Z):** User has not yet signed off on the green-gate.yml fix. Pivots posted to 3 Slack threads telling Hermes to pause Gate 8 work and wait for the fix. The /goal "/babysit and ensure Prs go /green max 2 hours" is unachievable without this CI architecture fix first.

**Related:** [[project-2026-06-13_bq_logging_3pr_closeout]] — earlier work pattern showed green-gate.yml GATE-6/GATE-7 fixes need to ship as a separate PR, not on the lane PR.
