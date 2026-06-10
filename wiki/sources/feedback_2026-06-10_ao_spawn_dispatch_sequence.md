---
type: source
slug: feedback_2026-06-10_ao_spawn_dispatch_sequence
ingested: 2026-06-10
source: ~/.claude/projects/-Users-jleechan-projects-worldarchitect-ai/memory/feedback_2026-06-10_ao_spawn_dispatch_sequence.md
---

# Source: AO spawn dispatch sequence

Two-gate pre-flight for `ao spawn --claim-pr`:

1. **Project name resolution**: don't guess from repo slug. Use `ao session ls` to get the exact name (`worldarchitect` not `worldarchitect.ai`).
2. **Lifecycle must be running**: `ao start --no-dashboard` first or spawn fails with "AO is not running".
3. **Verify after spawn**: read `session.json` for `agent` + `runtimeHandle.data.launchCommand`; if user asked for `--agent codex`, the launched command must literally be `codex`.

See memory file for the 4-step recipe and the failure modes that motivated it.
