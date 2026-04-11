---
title: "PR #173: refactor: 4-phase orchestration & LaunchAgent simplification (Phases 1–4 complete)"
type: source
tags: []
date: 2026-03-15
source_file: raw/prs-worldai_claw/pr-173.md
sources: []
last_updated: 2026-03-15
---

## Summary
The openclaw harness had accumulated significant structural debt across two dimensions:

1. **LaunchAgent sprawl** — 25+ plist files across `launchd/`, many orphaned (exit 127, stale gateway version, disabled with no re-enable path, double-dispatching webhooks). Each agent had its own restart logic, env block, and scheduling interval copy-pasted verbatim.

2. **Webhook pipeline fragmentation** — the GitHub webhook path was split across 8 files (`webhook_daemon.py`, `webhook_bridge.py`, `webhook_

## Metadata
- **PR**: #173
- **Merged**: 2026-03-15
- **Author**: jleechan2015
- **Stats**: +2756/-210 in 17 files
- **Labels**: none

## Connections
