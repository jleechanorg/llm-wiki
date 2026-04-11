---
title: "PR #344: [P2] chore: delete ao-pr-poller.sh and all references"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-344.md
sources: []
last_updated: 2026-03-21
---

## Summary
The `ao-pr-poller.sh` script was the original shell-script-based PR polling path for the AO orchestration system. It has been superseded by the **canonical scheduling path: OpenClaw gateway cron + AO lifecycle-worker**. References to the deprecated script remain scattered across the codebase, creating confusion about which scheduling path is current.

## Metadata
- **PR**: #344
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +13/-139 in 9 files
- **Labels**: none

## Connections
