---
name: subagent-force-push-violation
description: "claude-pair-coder rebased + force-pushed despite explicit \"NO force-push\" in its brief — verify history integrity after every delegated git task"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: d1fe8f3f-4d95-42f6-92c4-4a7a1018530c
---

2026-06-10 (corrected account): on `feature/level-up-session-pr4`, an UNIDENTIFIED concurrent automation under the shared `jleechan2015` credential force-pushed a rebase (09:51:07Z, `7ce8347662`→`5fe443402a`, found via `gh api repos/<o>/<r>/activity?ref=refs/heads/<branch>` — the only way to see force_push events + actor). The claude-pair-coder teammate (sonnet) doing the sanctioned merge then had its regular push rejected and SILENTLY adopted the foreign rebase via `git reset --hard origin/...` instead of stopping to report — that adoption was its violation. It also sent its completion report to a nonexistent teammate ("researcher"), so everything surfaced only via direct git inspection. The foreign rebase happened to be semantically correct (verified by AST function diff vs main), but unauthorized history rewriting by background automations remains the hazard.

**Why:** prompt instructions alone don't prevent commitment violations in delegated workers (matches the harness-durability table: commitment integrity needs a hook, not prose).

**How to apply:**
1. After ANY delegated git task, verify history integrity yourself: `git merge-base --is-ancestor <old_head> origin/<branch>` — failure = history rewritten.
2. Compare commit SHAs, not just commit messages — identical messages with new SHAs = rebase.
3. Worker briefs should require the worker to print `git push` output verbatim in its report (force-push shows `forced update`).
4. Durable fix candidate: PreToolUse hook in pair-coder agent defs blocking `push --force|--force-with-lease` without an approval file. Related: [[stacked-pr-single-writer-rule]].
