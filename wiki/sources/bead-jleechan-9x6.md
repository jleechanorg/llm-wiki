---
title: "harness2: Fix benchmark live flow - two bugs fixed, one remaining"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-9x6"
priority: P1
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [bug]** harness2: Fix benchmark live flow - two bugs fixed, one remaining

## Details
- **Bead ID:** `jleechan-9x6`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

## Session Summary (branch: harness2, PR #5648)

### Goal
Make both legacy (/pair) and pairv2 benchmark paths succeed end-to-end when running `benchmark_pair_executors.py --coder-cli claude --verifier-cli claude --parallel`.

### Bugs Fixed (committed & pushed)

**Fix 1 (commit 2ae0fbe): Text mismatch in readiness detection**
- `_wait_for_agent_launch_readiness` checked for "SESSION COMPLETION SUMMARY" but direct-prompt + lite-mode prints "AGENT CREATION RESULTS"
- Fixed by matching both strings and broadening regex `r"Successful(?:\s+Agents)?:\s+(\d+)"`
- Added 5 tests in `TestReadinessDetection`

**Fix 2 (commit 9c50bac): Buffer flush race**
- Python block-buffers stdout when redirected to file; readiness loop breaks on `process.poll()` non-None before content flushed to disk
- Fixed by adding 0.3s delay + post-exit log read after process termination
- Test: `test_post_exit_read_catches_late_flush`

**Fix 3 (commit d0c1c07 = current HEAD): pairv2 missing shared tmux socket**
- `_launch_live_pair_session` in `pair_execute_v2.py` did not set `ORCHESTRATION_TMUX_SOCKET` env var
- Each agent landed on its own `orch-{pid}-{timestamp}` socket; monitor got `tmux_sockets=None` and failed to find verifier → marked as failed after 3 grace checks
- Fixed: set `ORCHESTRATION_TMUX_SOCKET = session_id.replace("pair-", "")` before agent launch, pass `tmux_sockets=[pair_socket]` to monitor
- Added 2 tests in `PairV2TmuxSocketTests`
- All 90 tests pass (64 pair_execute + 26 pairv2/benchmark)

### Remaining Issue
After fix 3, pairv2 coder agent still fails with `process_exited` (no ready signal within startup window). The orchestration log ends abruptly after the /tmp directory listing (line 30), indicating the process crashes silently before agent creation.

**Hypothesis**: Too many stale processes (~121 running agents from previous benchmark runs) or a resource exhaustion. Note: the worktree `orch_worldarchitect.ai/test-debug-agent` exists from a manual debug run.

**Context**: Legacy path works fine (both agents launch, session stays in_progress during 120s window = expected). pairv2 fails at coder launch, not monitor detection.

### Next Steps
- Investigate why orchestration process exits after /tmp listing in pairv2 context
- Check if stale worktrees/processes are causing resource exhaustion
- Clean stale processes (NOT worktrees - do not delete worktrees)
- Re-run benchmark after cleanup

