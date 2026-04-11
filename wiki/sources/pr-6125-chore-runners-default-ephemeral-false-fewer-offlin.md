---
title: "PR #6125: chore(runners): default EPHEMERAL=false (fewer offline ghost registrations)"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6125.md
sources: []
last_updated: 2026-04-09
---

## Summary
Slack thread context: `EPHEMERAL=true` (previous default in `start-runner.sh`) makes each runner deregister after **one** job; Docker `--restart unless-stopped` brings containers back with **new** random names while old registrations stay **offline** in GitHub — looks like runners are broken when capacity is fine.

## Metadata
- **PR**: #6125
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +16/-8 in 4 files
- **Labels**: none

## Connections
