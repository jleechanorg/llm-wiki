---
title: "Feedback 2026 06 10 Smoke Mode Ci Guards"
type: source
tags: [memory, ao-worker, codex-worker, 2026-06]
date: 2026-06-10
source_file: .claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_smoke_mode_ci_guards.md
---

## Summary

**Classification**: Mandatory

PR [#7242](https://github.com/jleechanorg/worldarchitect.ai/pull/7242) fixed a regression where `/smoke` PR comments routed to mock Gemini silently. The fix had no guards, so the same regression could recur undetected. PR [#7446](https://github.com/jleechanorg/worldarchitect.ai/pull/7446) added three guards.

## Original

## Learning: Smoke Mode Routing Guards (2026-06-10)

**Classification**: Mandatory

PR [#7242](https://github.com/jleechanorg/worldarchitect.ai/pull/7242) fixed a regression where `/smoke` PR comments routed to mock Gemini silently. The fix had no guards, so the same regression could recur undetected. PR [#7446](https://github.com/jleechanorg/worldarchitect.ai/pull/7446) added three guards.

### Guard architecture

Two separate mock-enforcement mechanisms exist in `mcp-smoke-tests.yml`:
1. `determine-smoke-mode.sh` — handles `issue_comment` / `workflow_dispatch` paths
2. Hardcoded `env: TEST_MODE: mock` block in `try-self-hosted` job — handles `workflow_run` (auto-deploy) path

These are independent; a fix to one doesn't protect the other.

### Three guards (PR #7446)

**Guard 1 — Runtime assertion in `determine-smoke-mode.sh`:**
```bash
if [[ "$EVENT_NAME" = "issue_comment" && -z "$MANUAL_MODE_LOWER" && "$TEST_MODE" != "real" ]]; then
  echo "::error::smoke-mode invariant violated: ..." >&2
  exit 1
fi
```
Fires immediately at routing step if `issue_comment` + no mode → non-real.

**Guard 2 — Workflow call grep gate (in `smoke-mode-routing-contract` CI job):**
```bash
count=$(grep -c 'determine-smoke-mode.sh' .github/workflows/mcp-smoke-tests.yml)
[ "$count" -lt 2 ] && exit 1
```
Catches the script call being removed from the workflow.

**Guard 3 — try-self-hosted env grep gate (in `smoke-mode-routing-contract` CI job):**
```bash
grep -A 12 'MCP Server Smoke Tests \[Mock APIs\]' .github/workflows/mcp-smoke-tests.yml | grep -q 'TEST_MODE: mock' || exit 1
```
Catches the hardcoded mock block being removed from the auto-deploy job.

### /es exception for scripts/CI-only changes

For changes touching only `scripts/**` and `.github/**` (no `mvp_site/**`), the evidence standard exception applies: contract-test-level proof (`Smoke Mode Routing Contract: SUCCESS` in CI) is sufficient. No real-LLM `/es` bundle required.

### Coverage gap

Guards protect the two existing paths. A brand-new `workflow_run`-triggered job added in the future with no `TEST_MODE: mock` would NOT be caught. Acceptable for now given complexity vs. risk.

### References
- PR #7242 merge SHA: `25f6c5fb004609d906ef136008d8799640b3bd8a`
- PR #7446: https://github.com/jleechanorg/worldarchitect.ai/pull/7446
- Test PR #7445 (verification, closed): https://github.com/jleechanorg/worldarchitect.ai/pull/7445
- Contract tests: `scripts/test_determine_smoke_mode.sh` — 10 cases, all pass
- Bead: rev-k8jq1
