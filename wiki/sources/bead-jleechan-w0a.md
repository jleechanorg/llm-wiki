---
title: "Clean up git history (remove exposed credentials)"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-w0a"
priority: P2
issue_type: task
status: open
created_at: 2026-02-19
updated_at: 2026-02-19
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [task]** Clean up git history (remove exposed credentials)

## Details
- **Bead ID:** `jleechan-w0a`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-02-19
- **Updated:** 2026-02-19
- **Author:** jleechan
- **Source Repo:** .

## Description

The exposed credentials were committed to git history in commits like a853c71... and aa4a346....

Options:
1. Use GitHub's secret scanning unblock (fast but leaves history)
2. Rewrite history with git filter-branch or bfg (thorough but requires force push)

To rewrite history:
```bash
# Option 1: BFG Repo-Cleaner
brew install bfg
bfg --delete-files "*.jsonl" --no-blob-protection
git reflog expire --expire=now --all && git gc --prune=now --aggressive

# Option 2: GitHub support
# Contact GitHub support to remove sensitive data
```

Then force push: git push --force

