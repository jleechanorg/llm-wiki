---
name: ao-spawn-dispatch-sequence
description: ao spawn --claim-pr requires (1) correct project name from `ao session ls`, not guess; (2) ao start --no-dashboard first or "AO is not running" error
metadata:
  node_type: memory
  type: feedback
  originSessionId: accc5a5a-bae2-4e3c-96aa-4caa512ea998
---

When dispatching an AO worker via `ao spawn --claim-pr <N>`, two prerequisite gates must be hit in order or the spawn fails with confusing errors:

1. **Project name resolution**: `ao spawn --project <X>` rejects unknown project names with `"Unknown project: <X>"`. Don't guess the project name from the repo slug (e.g., `worldarchitect.ai` ≠ `worldarchitect`). Always run `ao session ls` (or `ao project ls`) first and copy the EXACT project identifier that appears in the active session list. For worldarchitect.ai the correct value is `worldarchitect`, not `worldarchitect.ai` or `jleechanorg/worldarchitect.ai`.

2. **Lifecycle must be running**: `ao spawn` returns `"✗ AO is not running — lifecycle polling is inactive."` if no orchestrator process is alive. Run `ao start --no-dashboard` first to bring the lifecycle manager up; only then does `ao spawn` succeed. `--no-dashboard` is preferred in tmux/CI sessions where a TUI would block the terminal.

3. **Verify after spawn**: per `~/.claude/CLAUDE.md` "Agent Orchestrator parameter fidelity" — read the spawned session's metadata before trusting it. Check `~/.agent-orchestrator/.../sessions/<id>/session.json` for `agent=<expected>` and `runtimeHandle.data.launchCommand` contains the expected CLI. If the user asked for Codex workers (`--agent codex`), the launchCommand must literally be `codex`, not `claude`/`gemini`/fallback.

**Why**: First AO spawn for PR #7386 failed twice — first with "Unknown project: worldarchitect.ai" (wrong guess from repo name), then with "AO is not running" (lifecycle never started). Both were 5-second mistakes but blocked the dispatch. The fix order is canonical: list existing sessions → start lifecycle → spawn with verified project name → verify launched command.

**How to apply**: Pre-flight checklist before `ao spawn`:
```bash
ao session ls | head -5                              # 1. get exact project name
ao start --no-dashboard                              # 2. start lifecycle (idempotent)
ao spawn --project <exact-from-ls> --claim-pr <N>     # 3. dispatch
cat ~/.agent-orchestrator/.../sessions/<id>/session.json | jq '.agent,.runtimeHandle.data.launchCommand'  # 4. verify
```

**Related**: `feedback_2026-06-10_pr_head_branch_force_push_rename.md` (the other half of the retarget workflow); `~/.claude/CLAUDE.md` "Agent Orchestrator parameter fidelity".
