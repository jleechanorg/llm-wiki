---
title: "PR #1948: Centralize Codex automation intro text"
type: source
tags: [codex]
date: 2025-11-05
source_file: raw/prs-worldarchitect-ai/pr-1948.md
sources: []
last_updated: 2025-11-05
---

## Summary
- centralize the Codex automation intro text in `codex_config` and expose helpers for formatting assistant mentions
- reuse the shared intro builder when composing PR monitor comments to avoid string drift
- update the targeting test to assert against the shared intro helper instead of a duplicated literal

## Metadata
- **PR**: #1948
- **Merged**: 2025-11-05
- **Author**: jleechan2015
- **Stats**: +97/-6 in 3 files
- **Labels**: codex

## Connections
