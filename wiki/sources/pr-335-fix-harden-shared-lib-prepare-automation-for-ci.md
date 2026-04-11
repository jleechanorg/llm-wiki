---
title: "PR #335: fix: harden shared-lib prepare automation for CI"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-335.md
sources: []
last_updated: 2025-10-13
---

## Summary
- add a guard script that only rebuilds shared libraries when dependencies are installed and persists the source hash
- point each shared library package's prepare hook at the guarded helper to avoid failing npm ci lifecycles
- restore the test-environment authenticated rate limit default to 20 requests so CI expectations remain accurate

## Metadata
- **PR**: #335
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +139/-5 in 6 files
- **Labels**: codex

## Connections
