---
title: "PR #1747: Normalize compose command output spacing"
type: source
tags: [codex]
date: 2025-09-27
source_file: raw/prs-worldarchitect-ai/pr-1747.md
sources: []
last_updated: 2025-09-27
---

## Summary
- normalize aggregated slash command strings before composing output in the compose hook
- trim deduplicated nested and combined command lists so user-visible messages no longer contain extra spaces
- add a regression test covering /pr single-command composition without relying on hardcoded allowlists

## Metadata
- **PR**: #1747
- **Merged**: 2025-09-27
- **Author**: jleechan2015
- **Stats**: +32/-9 in 2 files
- **Labels**: codex

## Connections
