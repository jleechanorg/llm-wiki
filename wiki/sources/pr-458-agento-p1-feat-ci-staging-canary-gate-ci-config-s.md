---
title: "PR #458: [agento] [P1] feat(ci): staging-canary-gate — CI config/schema checks before merge (orch-1ps.3)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-458.md
sources: []
last_updated: 2026-03-31
---

## Summary
Implements the **CI gate** (Stage 3) of the 3-stage staging pipeline design from Slack #C0AJ3SD5C79 (orch-1ps epic).

- Adds `.github/workflows/staging-canary-gate.yml` — runs on every PR open/sync/reopen
- Runs **portable canary checks** (schema validation, crash-keys, SDK version) directly in GitHub Actions
- Posts a **PR comment table** with PASS/FAIL per check
- **Blocks merge** on any FAIL (exit 1)
- Documents the **manual gate requirement** for gateway-dependent checks (health, Slack conne

## Metadata
- **PR**: #458
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +249/-6 in 2 files
- **Labels**: none

## Connections
