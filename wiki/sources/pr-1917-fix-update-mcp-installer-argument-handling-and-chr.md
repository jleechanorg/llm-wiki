---
title: "PR #1917: fix: update MCP installer argument handling and Chrome stats"
type: source
tags: [codex]
date: 2025-10-30
source_file: raw/prs-worldarchitect-ai/pr-1917.md
sources: []
last_updated: 2025-10-30
---

## Summary
- normalize installer arguments so `--dry-run` still maps to `--test` while preserving product selection and pass-through flags
- restore Grok defaults and forward CLI arguments when invoking the shared installer for Claude, Codex, or both
- track Chrome Superpowers installation outcomes in the aggregated MCP statistics

## Metadata
- **PR**: #1917
- **Merged**: 2025-10-30
- **Author**: jleechan2015
- **Stats**: +53/-9 in 2 files
- **Labels**: codex

## Connections
