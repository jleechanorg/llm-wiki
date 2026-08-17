---
title: "Firebase admin-app divergence needs real-Firestore tests (2026-08-15)"
type: source
tags: [feedback, testing, mcp, firebase, worldarchitect]
date: 2026-08-15
source_file: feedback_2026-08-15_firebase_admin_app_divergence_real_firestore_tests.md
---

## Summary

Bugs whose root cause lives in the seam between service identities (e.g. two
Firebase admin apps, divergent Firestore clients, async boundaries) cannot be
caught by Layer 1 unit tests alone. Pair any such fix with an integration-layer
test that drives the tool through its real dispatch path. Confirmed RED→GREEN
cycle on the WorldAI MCP `admin_download_campaign_entries` fix (bead
`rev-t6mtv`).

## Key Claims

- A pure Layer 1 unit test that mocks two clients the same way **cannot**
  reproduce a service-integration glue bug; the mocks must diverge.
- The fix routes through the canonical `firestore_service.get_db()` instead
  of the dedicated `worldai-tools-local-firestore` admin app — same path used
  by `scripts/download_campaign.py`.
- Regression coverage requires **two** tests: a Layer 1 test with divergent
  mocks AND a Layer 2 E2E test that drives the tool through
  `WorldAIToolsProxy.handle_jsonrpc` (or the equivalent real dispatch path).
- "Tests pass" ≠ "tests sufficient." Confirm RED by reverting the fix; if the
  regression tests don't fail without the fix, they don't catch the regression.
- The generic principle (Candidate C, research-backed) belongs in
  `AGENTS.md`; the failure-class taxonomy belongs in
  `.claude/skills/testing-layers/SKILL.md`.

## Key Quotes

> A mocked unit test cannot reproduce a bug whose root cause lives across a
> service boundary (multiple service identities, divergent clients, async
> boundaries). Pair such fixes with an integration-layer test.
> — `AGENTS.md` line ~49 (added 2026-08-15)

> Bugs whose root cause is service-integration glue (multiple Firebase admin
> apps, divergent Firestore clients, async boundaries) **cannot be caught by
> Layer 1 unit tests alone**, even with mocks. Mocks can simulate the
> divergence but cannot prove the real client behaves that way.
> — `.claude/skills/testing-layers/SKILL.md` "Service-Integration Glue Bugs"

## Connections

- [[WorldArchitectAI]] — repo where this fix and lesson originated
- [[TestingLayersSkill]] — the canonical owner of test-layer selection; this
  lesson adds a "Service-Integration Glue Bugs" subsection
- [[RootCauseFirstEngineering]] — same investigation discipline; the fix used
  `firestore_service.get_campaign_by_id` (the canonical shared helper) instead
  of patching the broken path
- [[TDDDiscipline]] — explicit TDD red-green-refactor discipline; this fix
  violated it and the lesson encoded the missing check
- [[Memory: feedback_2026-08-15_firebase_admin_app_divergence_real_firestore_tests]]
  — Claude auto-memory entry
- [[Bead: rev-t6mtv]] — the original bug
- [[Bead: rev-5n114]] — the learning bead (closed)

## Files Touched

- `mvp_site/worldai_tools_mcp_proxy.py` — `_tool_admin_download_campaign_entries`
  refactored to use `firestore_service.get_db()` via new helper
  `_download_campaign_story_entries_with_ids`.
- `mvp_site/tests/test_worldai_tools_mcp_proxy.py` — added two regression
  tests (canonical-path-via-mock-divergence, entry_ids filter via canonical path).
- `mvp_site/tests/test_end2end/test_worldai_admin_download_entries_end2end.py`
  — Layer 2 E2E test driving the tool through `handle_jsonrpc`.
- `.claude/skills/testing-layers/SKILL.md` — added "Service-Integration Glue
  Bugs" subsection with the taxonomy + reference incident.
- `AGENTS.md` — added the one-line generic principle (Candidate C from
  research).

## Verification

- **RED** (fix reverted): all 3 regression tests failed
  (`test_download_entries_uses_canonical_db_when_proxy_db_sees_no_story`,
  `test_download_entries_entry_ids_filter_via_jsonrpc`,
  `test_admin_download_campaign_entries_uses_canonical_path`).
- **GREEN** (fix applied): 30 passed (28 unit + 2 Layer 2 E2E), 4 skipped
  (pre-existing), no regressions.