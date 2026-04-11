---
title: "PR #416: [agento] [P2] feat(ao-manager): unified launchd manager for all AO components"
type: source
tags: []
date: 2026-03-27
source_file: raw/prs-worldai_claw/pr-416.md
sources: []
last_updated: 2026-03-27
---

## Summary
- Add `ao-manager.sh` — a single manager script that starts and monitors all AO components
- Add `ao-manager-notifier.sh` — wrapper that launches the notifier for the manager
- Add `install-ao-manager.sh` — bootstrap/uninstall script for the launchd plist
- Update `launchd/ai.agento-manager.plist.template` — now calls `ao-manager.sh` directly (previously had inline bash with hardcoded project list)

## Metadata
- **PR**: #416
- **Merged**: 2026-03-27
- **Author**: jleechan2015
- **Stats**: +521/-53 in 4 files
- **Labels**: none

## Connections
