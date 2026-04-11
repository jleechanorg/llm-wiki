---
title: "PR #74: feat(agento): Agent-Orchestrator integration via keyword routing"
type: source
tags: []
date: 2026-03-10
source_file: raw/prs-worldai_claw/pr-74.md
sources: []
last_updated: 2026-03-10
---

## Summary
- Adds AO (Agent-Orchestrator) as an alternative dispatch path, triggered by saying "agento" in OpenClaw chat
- OpenClaw LLM decides at inference time whether to use mctrl (bead-native) or agento (GitHub-native AO)
- Verified end-to-end: webhook → Slack delivery working

## Metadata
- **PR**: #74
- **Merged**: 2026-03-10
- **Author**: jleechan2015
- **Stats**: +347/-7 in 5 files
- **Labels**: none

## Connections
