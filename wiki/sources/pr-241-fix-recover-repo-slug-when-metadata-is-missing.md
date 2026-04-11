---
title: "PR #241: fix: recover repo slug when metadata is missing"
type: source
tags: [codex]
date: 2025-10-09
source_file: raw/prs-/pr-241.md
sources: []
last_updated: 2025-10-09
---

## Summary
- capture the repository root/dirname so the Codex setup script can infer the slug contextually
- add a GitHub API fallback that looks up repositories accessible to the token when no remote or metadata is available

## Metadata
- **PR**: #241
- **Merged**: 2025-10-09
- **Author**: jleechan2015
- **Stats**: +193/-0 in 1 files
- **Labels**: codex

## Connections
