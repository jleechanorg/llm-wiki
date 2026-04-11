---
title: "PR #278: fix: verdict comment markers + fail-closed evidence gates"
type: source
tags: []
date: 2026-03-19
source_file: raw/prs-worldai_claw/pr-278.md
sources: []
last_updated: 2026-03-19
---

## Summary
PR #269 added Phase 2 reviewer loop — reviewer_agent posts GitHub reviews and MCP mail. But GitHub blocks APPROVED reviews on your own PRs (HTTP 422). This PR switches from APPROVED reviews to machine-readable verdict comment markers that merge_gate reads from issue comments. Also fixes several fail-open bugs in merge_gate.

## Metadata
- **PR**: #278
- **Merged**: 2026-03-19
- **Author**: jleechan2015
- **Stats**: +206/-6 in 4 files
- **Labels**: none

## Connections
