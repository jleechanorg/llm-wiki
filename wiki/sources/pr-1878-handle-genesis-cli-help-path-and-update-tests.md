---
title: "PR #1878: Handle Genesis CLI help path and update tests"
type: source
tags: [codex]
date: 2025-10-17
source_file: raw/prs-worldarchitect-ai/pr-1878.md
sources: []
last_updated: 2025-10-17
---

## Summary
- add a dedicated GenesisHelpRequested exception so -h/--help exits successfully while reusing shared usage output
- update the shared usage copy to avoid duplicate Codex notes and expose the standard help alias across runners
- extend CLI unit tests to cover help handling alongside the parser updates

## Metadata
- **PR**: #1878
- **Merged**: 2025-10-17
- **Author**: jleechan2015
- **Stats**: +857/-79 in 7 files
- **Labels**: codex

## Connections
