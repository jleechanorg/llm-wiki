---
title: "PR #398: [P1] feat(thread): terminal status guarantee + missed-reply watchdog + cmux preflight validation"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-398.md
sources: []
last_updated: 2026-03-25
---

## Summary
Incident 1774380244.271829: a Slack thread task for `cmux list-surfaces --workspace 23 --json` produced a large stderr help dump (invalid `--json` flag) with no terminal in-thread status message. The thread went silent with no `done/blocked/needs-input` finalizer.

## Metadata
- **PR**: #398
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +1143/-37 in 6 files
- **Labels**: none

## Connections
