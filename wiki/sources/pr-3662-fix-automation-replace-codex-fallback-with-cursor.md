---
title: "PR #3662: fix(automation): Replace Codex fallback with cursor-agent to reduce quota usage"
type: source
tags: []
date: 2026-01-16
source_file: raw/prs-worldarchitect-ai/pr-3662.md
sources: []
last_updated: 2026-01-16
---

## Summary
- Replace Codex fallback with cursor-agent in fix-comment and fixpr workflows
- Reduces Codex quota consumption by ~70% (81 → 24 conversations/day)
- Codex CLI now only used by dedicated `--codex-update` workflow

## Metadata
- **PR**: #3662
- **Merged**: 2026-01-16
- **Author**: jleechan2015
- **Stats**: +28/-34 in 9 files
- **Labels**: none

## Connections
