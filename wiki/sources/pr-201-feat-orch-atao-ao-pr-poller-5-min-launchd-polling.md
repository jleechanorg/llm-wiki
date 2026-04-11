---
title: "PR #201: feat(orch-atao): ao-pr-poller — 5-min launchd polling daemon"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-201.md
sources: []
last_updated: 2026-03-16
---

## Summary
- ao-pr-poller.sh: polls all jleechanorg repos every 5 min, spawns agento on non-green PRs with no active AO session
- ai.ao-pr-poller.plist: launchd agent with StartInterval=300, correct PATH/HOME
- Rate-cap: max 10 respawns per 12h rolling window per PR (state in /tmp/ao-pr-poller-caps.json)
- Manual override: touch /tmp/ao-pr-poller-override-REPO_N resets that PR's cap
- Design doc: roadmap/AO_PR_POLLLER_DESIGN.md

## Metadata
- **PR**: #201
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +247/-0 in 4 files
- **Labels**: none

## Connections
