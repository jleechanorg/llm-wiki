---
title: "PR #93: feat: companion action persistence (WC-9rl)"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-93.md
sources: []
last_updated: 2026-03-26
---

## Summary
Companion actions (movements, interactions, decisions) need to survive server restarts. The core persistence layer (schema, saveCompanionAction, getActionsSince, tick-save in runSimulation) was already in place. This PR fills the remaining gaps.

## Metadata
- **PR**: #93
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +408/-42 in 5 files
- **Labels**: none

## Connections
