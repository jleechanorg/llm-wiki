---
title: "PR #375: [agento] fix(evidence-gate): accept both **label**: and **label:** markdown formats"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-375.md
sources: []
last_updated: 2026-04-04
---

## Summary
The `evidence-gate.yml` workflow uses `grep -F` (fixed-string) and `awk` regex patterns to detect evidence labels like `**Repro gist:`, `**Terminal test output:`, `**Terminal media:`, and `**UI media:`. However, AO workers produce these labels in standard markdown bold format with closing `**` before the colon: `**Repro gist:**`. The fixed-string patterns don't match this format, causing false negatives on all 4 evidence checks for properly-formatted PRs.

## Metadata
- **PR**: #375
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +9/-9 in 1 files
- **Labels**: none

## Connections
