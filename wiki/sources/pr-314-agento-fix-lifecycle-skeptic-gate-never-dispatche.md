---
title: "PR #314: [agento] fix(lifecycle): skeptic gate never-dispatches for first-seen and ci_failed sessions (wc-zsw)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-314.md
sources: []
last_updated: 2026-03-31
---

## Summary
The skeptic gate GHA workflow posts a trigger comment and polls for VERDICT, but lifecycle-manager was silently failing to dispatch skeptic for two cases.

## Metadata
- **PR**: #314
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +304/-119 in 5 files
- **Labels**: none

## Connections
