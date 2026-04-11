---
title: "PR #173: fix: guard Husky prepare script during Docker builds"
type: source
tags: [codex]
date: 2025-11-10
source_file: raw/prs-/pr-173.md
sources: []
last_updated: 2025-11-10
---

## Summary
- guard the Husky prepare script so Docker/CI builds exit cleanly when devDependencies are omitted
- fail fast with an explicit error message if Husky is installed but the install step errors for another reason

## Metadata
- **PR**: #173
- **Merged**: 2025-11-10
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: codex

## Connections
