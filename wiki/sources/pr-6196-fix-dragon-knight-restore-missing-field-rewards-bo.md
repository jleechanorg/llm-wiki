---
title: "PR #6196: fix(dragon-knight): restore missing FIELD_REWARDS_BOX in template extraction (REV-rnz)"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldarchitect-ai/pr-6196.md
sources: []
last_updated: 2026-04-11
---

## Summary
User insisted "rewards_box was broken **before** PR #6161" and pointed at PR #6137 as the suspect. Deep subagent investigation confirmed: PR #6137 (`abd799c2e`, merged 2026-04-09 — two days before #6161) introduced the Dragon Knight template bypass in `mvp_site/world_logic.py:5012-5038` but silently omits `FIELD_REWARDS_BOX` from the extraction dict.

## Metadata
- **PR**: #6196
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +113/-0 in 2 files
- **Labels**: none

## Connections
