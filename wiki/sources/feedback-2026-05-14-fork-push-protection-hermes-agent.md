---
name: Fork Push Protection — hermes-agent
description: jleechanclaw fork has old openclaw commits with secrets; use clean branch from hermes/main for all upstream PRs
type: feedback
date: 2026-05-14
raw: raw/feedback_2026-05-14_fork-push-protection-hermes-agent.md
---

## Summary

In `jleechanorg/hermes-agent` worktrees, the `origin` remote (`jleechanclaw`) contains pre-migration openclaw commits with embedded API keys. GitHub Push Protection blocks pushing those commits to the canonical `hermes` remote (`jleechanorg/hermes-agent`).

## Rule

Always use `fix/*` or `feat/*` branches based on `hermes/main` for PRs against `jleechanorg/hermes-agent`. Never push `session/ha-*` directly to `hermes`.

```bash
git checkout -b fix/<topic> hermes/main
git cherry-pick <fix-sha>
# resolve conflict if .gitignore differs
git push hermes fix/<topic>
```

## References

- PR #13: https://github.com/jleechanorg/hermes-agent/pull/13
- Commit: `c589b00f` (fix/gitignore-ao-bearer-token)
- Bead: `orch-havc` (CLOSED 2026-05-14)
