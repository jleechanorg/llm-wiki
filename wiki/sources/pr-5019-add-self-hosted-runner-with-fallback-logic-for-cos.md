---
title: "PR #5019: Add: self-hosted runner with fallback logic for cost savings"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-worldarchitect-ai/pr-5019.md
sources: []
last_updated: 2026-02-08
---

## Summary
Builds on #4610 (merged) by adding intelligent fallback logic for workflows.

**Key improvements:**
- True fallback pattern: self-hosted (FREE) → GitHub-hosted (paid) with 2min timeout
- Production scripts for runner setup with intentional clock drift support
- 4 workflows converted: pr-cleanup, hook-tests, doc-size-check, mcp-smoke-tests

**Cost savings:** ~$6-15/month when self-hosted runner is available

## Metadata
- **PR**: #5019
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +1282/-16 in 12 files
- **Labels**: none

## Connections
