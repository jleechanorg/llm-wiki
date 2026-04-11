---
title: "PR #5887: automation: route native catch-up jobs through mctrl wrapper"
type: source
tags: []
date: 2026-03-09
source_file: raw/prs-worldarchitect-ai/pr-5887.md
sources: []
last_updated: 2026-03-09
---

## Summary
- route native launchd/systemd PR automation jobs through an `mctrl`-native wrapper instead of the old Mission Control naming
- keep wrapper `--exec` mode so scheduled jobs preserve exact `jleechanorg-pr-monitor` commands while emitting catch-up lifecycle metadata
- namespace per-job evidence/health files under `automation/evidence/mctrl` and mark native runs as `trigger_source=catch_up`

## Metadata
- **PR**: #5887
- **Merged**: 2026-03-09
- **Author**: jleechan2015
- **Stats**: +413/-90 in 4 files
- **Labels**: none

## Connections
