---
title: "PR #170: fix: remove __future__ annotations, update deps, fix test regression"
type: source
tags: []
date: 2026-02-02
source_file: raw/prs-/pr-170.md
sources: []
last_updated: 2026-02-02
---

## Summary
This PR fixes three critical bugs identified in the MCP Mail codebase:

1. **Pydantic NameError fix (HIGH)**: Remove `from __future__ import annotations` causing type resolution issues
2. **Security update (HIGH)**: Update fastmcp from 2.12.5 to >=2.14.0
3. **Compatibility fix (MEDIUM)**: Update authlib from <1.6 to >=1.6.5

Additionally, fixes a test regression caused by the dependency updates.

## Metadata
- **PR**: #170
- **Merged**: 2026-02-02
- **Author**: jleechan2015
- **Stats**: +808/-317 in 22 files
- **Labels**: none

## Connections
