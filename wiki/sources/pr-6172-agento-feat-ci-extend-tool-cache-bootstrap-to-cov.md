---
title: "PR #6172: [agento] feat(ci): extend tool-cache bootstrap to coverage, doc-size-check, hook-tests, mcp-smoke workflows"
type: source
tags: []
date: 2026-04-10
source_file: raw/prs-worldarchitect-ai/pr-6172.md
sources: []
last_updated: 2026-04-10
---

## Summary
- Apply `scripts/ci/setup-runner-tool-cache.sh` to all self-hosted workflows that call `actions/setup-python`, not just `test.yml`
- Prevents `/Users/runner` permission errors on self-hosted runners during Python setup

## Metadata
- **PR**: #6172
- **Merged**: 2026-04-10
- **Author**: jleechan2015
- **Stats**: +29/-3 in 5 files
- **Labels**: none

## Connections
