---
title: "PR #208: fix: restrict Python to 3.11-3.13, prevent Python 3.14 startup failures"
type: source
tags: []
date: 2026-02-08
source_file: raw/prs-/pr-208.md
sources: []
last_updated: 2026-02-08
---

## Summary
Fixes Python 3.14 incompatibility by implementing defense-in-depth protection against `collections.abc.ByteString` ImportError in the beartype dependency chain.

## Metadata
- **PR**: #208
- **Merged**: 2026-02-08
- **Author**: jleechan2015
- **Stats**: +286/-769 in 20 files
- **Labels**: none

## Connections
