---
title: "PR #855: Improve blast latency timing and adaptive concurrency"
type: source
tags: [codex]
date: 2025-11-27
source_file: raw/prs-/pr-855.md
sources: []
last_updated: 2025-11-27
---

## Summary
- measure blast request latency after reading the full response body to include streaming duration and clean up timeouts
- adjust BlastRunner worker pool to honor target QPS by spawning additional workers dynamically within max limits

## Metadata
- **PR**: #855
- **Merged**: 2025-11-27
- **Author**: jleechan2015
- **Stats**: +51/-25 in 1 files
- **Labels**: codex

## Connections
