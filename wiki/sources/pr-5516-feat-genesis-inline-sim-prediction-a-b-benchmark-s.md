---
title: "PR #5516: feat(genesis): inline /sim prediction + A/B benchmark script"
type: source
tags: []
date: 2026-02-14
source_file: raw/prs-worldarchitect-ai/pr-5516.md
sources: []
last_updated: 2026-02-14
---

## Summary
- Rewrote `/sim` to predict inline using existing conversation context — no JSONL parsing, no subprocess, no `claude -p` calls
- Added `/sim_async` preserving the old subprocess-based approach for offline comparison
- Added `genesis/scripts/sim_ab_benchmark.py` for offline A/B benchmarking (baseline vs v2.2 prompt with separate Sonnet instances, full 40-turn conversation history)

## Metadata
- **PR**: #5516
- **Merged**: 2026-02-14
- **Author**: jleechan2015
- **Stats**: +1072/-413 in 7 files
- **Labels**: none

## Connections
