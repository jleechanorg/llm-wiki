---
title: "PR #81: fix: remove double JSON serialization in tool handlers"
type: source
tags: []
date: 2025-11-09
source_file: raw/prs-/pr-81.md
sources: []
last_updated: 2025-11-09
---

## Summary
Fixed critical response formatting bug where tool handlers were returning JSON.stringify() results, causing double serialization when wrapped by the MCP transport layer.

## Metadata
- **PR**: #81
- **Merged**: 2025-11-09
- **Author**: jleechan2015
- **Stats**: +610/-55 in 5 files
- **Labels**: none

## Connections
