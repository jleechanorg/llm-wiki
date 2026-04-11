---
title: "PR #365: chore: hash shared-libs builds and drop dist artifacts"
type: source
tags: []
date: 2025-10-16
source_file: raw/prs-/pr-365.md
sources: []
last_updated: 2025-10-16
---

## Summary
- Implement content-hash-based build detection for shared-libs (replaces mtime checking)
- Remove dist/ artifacts from git (added to .gitignore)
- Add automatic rebuild triggers via npm prepare scripts
- Centralize hash computation in shared utility script

## Metadata
- **PR**: #365
- **Merged**: 2025-10-16
- **Author**: jleechan2015
- **Stats**: +51/-44 in 5 files
- **Labels**: none

## Connections
