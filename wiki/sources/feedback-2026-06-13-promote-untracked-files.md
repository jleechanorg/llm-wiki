---
title: "2026-06-13 Promote Untracked Files"
type: source
tags: ["feedback", "dark-factory"]
date: 2026-06-13
source_file: raw/feedback_2026-06-13_promote_untracked_files.md
---

## Summary
When `git status -s` shows untracked files, the \

## Key Claims
- When `git status -s` shows untracked files, the "rm + .gitignore" reflex is usually wrong. Run `git log --all -- <file>` first — if the file has commits anywhere (stale branch, abandoned PR, etc.), it's real work that got lost in the queue, not a stray artifact. The right move is to land it, not rm it.
- 1. `git status -s` shows `?? <path>` — DON'T immediately plan a cleanup PR.
- 2. `git log --all -- <path>` — does the file have commits anywhere? If yes, find the branch and inspect the commit. The on-disk version is usually newer than the branch copy (continuing work after a stale branch).
- 3. If untracked + no git history: ask "is this real work?" Read it. Run `./bin/conformance validate` if it's a `.dot`. If it parses, ships, and has the right contract (timeouts, etc.), it's a candidate for promotion.
- 4. If untracked + has stale-branch history: cherry-pick or re-create the work on a fresh branch off `main` (the stale branch is usually behind main and would rebase-conflict anyway).
- 5. **Never** `rm` an untracked file without asking the user. Real work is the most common reason for untracked files in this repo; "should we delete this" deserves explicit confirmation.

## Connections
- [[close-housekeeping-beads-at-the-start-of-any-what-next-decision]]
