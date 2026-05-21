---
title: "llm_inspector integrate no script"
type: source
tags: [integrate, llm-inspector, git, workflow, branch]
raw: raw/feedback_2026-05-14_llm-inspector-integrate-no-script.md
date: 2026-05-14
---

## Summary

`llm_inspector` has no `integrate.sh` script. `/integrate` must be executed manually using standard git commands. A stale local branch with the same name must be explicitly deleted before recreating.

## Manual Integrate Steps

```bash
git checkout main
git pull origin main
git branch -D <branch>           # if branch already exists locally
git checkout -b <branch>
git branch --set-upstream-to=origin/main <branch>
```

## Discovery Context

- Repo: `/Users/jleechan/projects_other/llm_inspector`
- Discovered 2026-05-14 while integrating PR #1 (`fix/anthropic-tool-schema`, merged 2026-05-14T21:00:56Z)
- Stale local branch `fix/anthropic-tool-schema` had to be deleted: `git branch -D fix/anthropic-tool-schema`
- New branch recreated from `85cb429` (squash-merged commit)

## Detection Pattern

Before running `/integrate` in any repo, check whether the script exists:
```bash
ls $(git rev-parse --show-toplevel)/integrate.sh 2>/dev/null && echo "script exists" || echo "manual steps required"
```

## Related Concepts

- [[Integrate]] — /integrate skill and integrate.sh workflow
