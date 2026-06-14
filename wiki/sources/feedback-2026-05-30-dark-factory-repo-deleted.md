---
title: "Feedback 2026-05-30 Dark Factory Repo Deleted"
type: source
tags: [feedback, project, agent-orchestrator, dark-factory, memory-file]
date: 2026-05-30
source_file: raw/memory_backfill_2026_06_13/feedback_2026-05-30_dark_factory_repo_deleted.md
---

## Summary

is the registered AO project clone ( in ). The lifecycle worker and all worktrees depend on it. The directory was deleted between 2026-05-24 and 2026-05-29.

## Key Claims

- Never `rm -rf ~/projects/dark-factory` without explicit user instruction naming this exact path
- If asked to "clean up disk space" or "reset the dark-factory repo", confirm before deleting this path
- If the path goes missing: `git clone https://github.com/jleechanorg/dark-factory ~/projects/dark-factory`
- Protected AO project paths (never auto-delete): `~/projects/dark-factory`, `~/projects/worldarchitect.ai`, `~/project_agento/agent-orchestrator`

## Key Quotes

_(No blockquotes in source)_

## Connections

_(No prior wiki links detected)_
