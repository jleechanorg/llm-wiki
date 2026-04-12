---
title: "harness2: Fix pairv2 coder process_exited - orchestration crashes after /tmp listing"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-kr6"
priority: P1
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [bug]** harness2: Fix pairv2 coder process_exited - orchestration crashes after /tmp listing

## Details
- **Bead ID:** `jleechan-kr6`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

## Next Steps: Fix remaining pairv2 benchmark failure

### Symptom
After fix 3 (shared tmux socket, commit d0c1c07), pairv2 coder agent fails with `process_exited` - no ready signal detected within startup window.

Orchestration log (`harness218357955cb97c5bccoder.log`) ends abruptly at line 30 (blank) after the /tmp directory listing, before any agent creation output. Process exits silently.

### Investigation needed

1. **Why does orchestration exit after /tmp listing?**
   - The /tmp listing comes from `task_dispatcher.py` `active_agents` property → `_get_active_tmux_agents()`
   - The crash happens right after this call (or during it)
   - Could be: subprocess timeout on tmux list-sessions with 100+ sockets, or Python exception swallowed somewhere

2. **Check stale process count**
   - At time of failure: ~121 processes matching `claude|orchestrat`
   - Too many active tmux sessions may cause `tmux list-sessions` to hang or error
   - Previous benchmark runs left agents running; cleanup needed (kill stale agent processes, NOT delete worktrees)

3. **Verify the crash is resource-related vs. code bug**
   - Run orchestration manually: `unset CLAUDECODE; venv/bin/python3 orchestration/orchestrate_unified.py --agent-cli claude --no-wrap-prompt --bead test --mcp-agent test-agent --lite-mode "test"` with many active tmux sockets
   - Check if /tmp listing shows more entries correlating with failures

### Approach
- Kill stale claude/orchestration processes from previous runs (NOT worktrees, NOT dirs)
- Re-run benchmark: `unset CLAUDECODE && venv/bin/python3 .claude/scripts/benchmark_pair_executors.py --coder-cli claude --verifier-cli claude --parallel --timeout-seconds 120`
- If still failing after cleanup, add error capture to `launch_coder_agent` subprocess stderr
- Check if `_get_active_tmux_agents` in task_dispatcher.py has a timeout issue with many sockets

### Success criteria
- pairv2 coder agent launches successfully (log shows "AGENT CREATION RESULTS" with Successful: 1/1)
- Monitor finds both agents on shared tmux socket
- Benchmark shows both legacy and pairv2 with session_status=timeout (both agents running within 120s window)

### Context
- Branch: harness2, PR #5648
- All 90 tests pass
- Legacy path works fine
- IMPORTANT: Do NOT delete any worktrees or directories

