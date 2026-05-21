---
name: llm-inspector-integrate-no-script
description: llm_inspector has no integrate.sh — /integrate must be done manually with git commands; stale local branch needs explicit deletion
metadata: 
  node_type: memory
  type: feedback
  bead: none
  originSessionId: f6c08ed2-9a66-45b2-9ecb-2784de0ecba6
---

## Rule

When running `/integrate` in `llm_inspector`, there is no `integrate.sh` script. Execute these steps manually:

```bash
git checkout main
git pull origin main
git branch -D <branch>           # if branch already exists locally
git checkout -b <branch>
git branch --set-upstream-to=origin/main <branch>
```

**Why:** llm_inspector is a small utility repo — no CI/branch automation scaffold. The stale local branch `fix/anthropic-tool-schema` had to be deleted with `git branch -D` before recreating from latest main.

**How to apply:** Any `/integrate` invocation in this repo skips the `./integrate.sh` step entirely and does the 5-command sequence above directly.

## Context

- Discovered 2026-05-14 while integrating PR #1 (`fix/anthropic-tool-schema`, merged 2026-05-14T21:00:56Z)
- Repo: `/Users/jleechan/projects_other/llm_inspector`
- Branch recreated from `85cb429` (squash-merged commit on main)
- After recreation: `fix/anthropic-tool-schema` tracks `origin/main`, clean state

## Reusable Pattern

Before running `/integrate` in any new repo, check:
```bash
ls $(git rev-parse --show-toplevel)/integrate.sh 2>/dev/null && echo "script exists" || echo "manual steps required"
```
