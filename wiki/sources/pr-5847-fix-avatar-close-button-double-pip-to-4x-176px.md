---
title: "PR #5847: fix: avatar close button + double pip to 4x (176px)"
type: source
tags: []
date: 2026-03-04
source_file: raw/prs-worldarchitect-ai/pr-5847.md
sources: []
last_updated: 2026-03-04
---

## Summary
### Fix: Close Button Not Working
The `cloneNode(true)` approach for preventing listener accumulation was detaching the close button from the DOM. When `cloneNode(true)` was called on the overlay, the close button reference (`closeBtn`) was captured BEFORE the overlay replacement, leaving it orphaned. Replaced with simple `onclick` property assignment which naturally replaces previous handlers.

### Feature: Double Avatar Pip to 4x
- Desktop: 88px → 176px
- Mobile: 72px → 144px

## Metadata
- **PR**: #5847
- **Merged**: 2026-03-04
- **Author**: jleechan2015
- **Stats**: +588/-37 in 5 files
- **Labels**: none

## Connections
