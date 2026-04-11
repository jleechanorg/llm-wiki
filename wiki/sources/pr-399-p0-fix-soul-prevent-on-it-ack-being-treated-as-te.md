---
title: "PR #399: [P0] fix(soul): prevent On-it ack being treated as terminal response (openclaw-silent-ack)"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-399.md
sources: []
last_updated: 2026-03-25
---

## Summary
On 2026-03-25, openclaw sent 'On it — checking ao:antig terminal' twice with no follow-through. Root cause analysis of sessions 8f95d93d-topic and 69675365-5d0c confirmed: SOUL.md told openclaw to post ack BEFORE work, and the model treated the ack as the terminal response.

## Metadata
- **PR**: #399
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
