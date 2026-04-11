---
title: "PR #99: Stop committing conversation client dist artifacts"
type: source
tags: [codex]
date: 2025-11-14
source_file: raw/prs-/pr-99.md
sources: []
last_updated: 2025-11-14
---

## Summary
- delete the generated `packages/conversation-client/dist` files and ignore future build output under packages
- add a `prepare` script so installing or linking the package rebuilds `dist` automatically and document the workflow in the README

## Metadata
- **PR**: #99
- **Merged**: 2025-11-14
- **Author**: jleechan2015
- **Stats**: +7/-4460 in 57 files
- **Labels**: codex

## Connections
