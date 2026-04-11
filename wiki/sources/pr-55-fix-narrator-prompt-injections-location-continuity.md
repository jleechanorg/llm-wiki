---
title: "PR #55: fix: narrator prompt injections, location continuity, AGGRESSIVE companion targeting"
type: source
tags: []
date: 2026-03-07
source_file: raw/prs-worldai_claw/pr-55.md
sources: []
last_updated: 2026-03-07
---

## Summary
- **Open threads injection** (LC-5as, LC-wb9, LC-spx, LC-ga9): `coup_progress` and `intel_level` thresholds dynamically inject scene-forcing threads into the system prompt — CONVERGENCE at ≥70, Jaehaerys pressure at ≥50/60, intel recon-complete shift at ≥80
- **Canon facts enforcement** (LC-5ef, LC-ddh): `canon_facts[]` in session state is injected as `[CANON_FACTS]` block that overrides LLM world-knowledge (Rhaenys gender, Aerys confinement, etc.)
- **Location continuity** (LC-0v7): System inst

## Metadata
- **PR**: #55
- **Merged**: 2026-03-07
- **Author**: jleechan2015
- **Stats**: +504/-6 in 8 files
- **Labels**: none

## Connections
