---
title: "PR #417: [P1] feat(memory): safe one-off mem0-purge script + runbook for Benjamin false memories"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-417.md
sources: []
last_updated: 2026-03-28
---

## Summary
There are 8 false mem0/Qdrant memories referencing a non-existent person "Benjamin" — created by errant LLM sessions that invented a fictional human collaborator. These pollute semantic search (score ~0.7+) and need to be deleted. The memory_delete tool is not available in the current runtime, so a careful manual script is required.

## Metadata
- **PR**: #417
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +1689/-21 in 16 files
- **Labels**: none

## Connections
