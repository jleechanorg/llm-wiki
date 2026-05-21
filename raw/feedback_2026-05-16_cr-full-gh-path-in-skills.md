---
name: cr-full-gh-path-in-skills
description: CodeRabbit CHANGES_REQUESTED on any skill file snippet using bare "gh" — must use ~/.local/bin/gh --repo owner/repo
type: feedback
bead: none
---

## Context

`.claude/skills/*.md` files have a house rule: use full absolute paths always (from CLAUDE.md). CodeRabbit enforces this on all new code snippets in skill files.

## Rule

Any command snippet in `.claude/skills/*.md` that uses `gh` must use:

```bash
~/.local/bin/gh pr view <PR_NUMBER> --repo jleechanorg/your-project.com ...
```

Not:
```bash
gh pr view <PR> ...   # WRONG — CR will CHANGES_REQUESTED
```

## Why

CodeRabbit reads CLAUDE.md's "Full absolute paths ALWAYS" rule and applies it to review skills files. A bare `gh` in a new snippet triggers a P2 "Use the same full-path and explicit-repo pattern" comment with CHANGES_REQUESTED.

## Observed in

PR #6942, 2026-05-16. Adding the `statusCheckRollup` jq snippet to `github-cli-reference.md` with bare `gh` → CR CHANGES_REQUESTED. Fixed with `~/.local/bin/gh ... --repo jleechanorg/your-project.com`.

**How to apply:** When adding any `gh` command to a WA skill file, always prefix with `~/.local/bin/gh` and add `--repo jleechanorg/your-project.com`.
