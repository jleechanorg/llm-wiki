---
title: "PR #485: [agento] feat(infra): staging/prod directory separation with deploy pipeline"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldai_claw/pr-485.md
sources: []
last_updated: 2026-04-04
---

## Summary
The gateway architecture previously lacked clean separation between staging and production. Changes applied directly to ~/.openclaw/ affected the live gateway immediately with no validation gate. Multiple P0 outages in March 2026 (config drift, native module ABI mismatches, Slack token issues) resulted from untested changes hitting production.

## Metadata
- **PR**: #485
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +658/-329 in 21 files
- **Labels**: none

## Connections
