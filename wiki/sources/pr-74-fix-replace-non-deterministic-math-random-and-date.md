---
title: "PR #74: fix: replace non-deterministic Math.random and Date.now in companion logic (WC-a22, wc-qh7)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-74.md
sources: []
last_updated: 2026-03-26
---

## Summary
Two P0 determinism bugs in `faction_simulator.ts` caused companion actions to produce different results on repeated calls with the same inputs. This breaks reproducibility for testing, debugging, and simulation replay.

## Metadata
- **PR**: #74
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +126/-9 in 2 files
- **Labels**: none

## Connections
