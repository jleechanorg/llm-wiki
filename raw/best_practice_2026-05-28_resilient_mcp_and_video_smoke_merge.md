---
name: Resilient MCP and Playwright video smoke test conflict resolution
description: Structured blend of branch-specific Playwright checks, cleanups, and main-refactored workflows to prevent environment and test failures.
type: feedback
bead: rev-2av80
---

## Context
When merging main branches into specialized bug-fix branches, line-by-line differences in test suites (e.g. `test_scroll_video_evidence.py` and `test_cache_cross_run_savings.py`) often conflict.

## Solution/Rule
1. **Never blindly choose one side of conflict markers.** Always synthesize branch-added environment cleanups (such as cleaning cache directories or starting telemetry parsers) with main's refactored structure.
2. **Implement pre-flight resilience.** When E2E or smoke tests depend on external browser engines like Playwright, wrap them in clean pre-flight checks (`chromium.launch`) or try-except blocks so that in restricted runner environments they skip gracefully (exit 0) rather than raising exceptions and failing the entire CI gate.
