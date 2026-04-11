---
title: "PR #412: [agento] [P2] feat(bd-z14m): Create a launchd KeepAlive plist for the OpenClaw gateway process"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-412.md
sources: []
last_updated: 2026-03-29
---

## Summary
The OpenClaw gateway previously ran without KeepAlive, meaning crashes or unexpected terminations left the gateway offline until manually restarted. This PR adds a proper macOS LaunchAgent plist with KeepAlive to ensure the gateway self-heals.

## Metadata
- **PR**: #412
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +149/-102 in 11 files
- **Labels**: none

## Connections
