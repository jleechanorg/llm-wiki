---
title: "PR #66: fix(config): block auto-merge reaction config"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-66.md
sources: []
last_updated: 2026-03-21
---

## Summary
- Add `validateNoAutoMergeReactions()` to `config.ts` that scans both global and per-project reactions for `action: auto-merge` and throws a descriptive error
- Wire the validation into `validateConfig()` after Zod parse
- Add 4 tests covering: global reaction rejection, per-project override rejection, multi-offender reporting, and allowlist of safe actions (notify, send-to-agent)

## Metadata
- **PR**: #66
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +165/-0 in 2 files
- **Labels**: none

## Connections
