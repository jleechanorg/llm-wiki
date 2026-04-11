---
title: "PR #359: fix: delete ao-pr-poller.sh (superseded by AO lifecycle-worker)"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-359.md
sources: []
last_updated: 2026-03-21
---

## Summary
The `ao-pr-poller.sh` script was a cron/launchd-based poller that scanned for non-green PRs and respawned AO agents. PR #322 deprecated the launchd plist (`ai.ao-pr-poller.plist.deprecated`) but left the script in place.

The AO lifecycle-worker now handles this natively — no separate poller needed.

## Metadata
- **PR**: #359
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +0/-576 in 1 files
- **Labels**: none

## Connections
