---
title: "PR #170: [agento] fix(agent-opencode): prevent false-positive waiting_input from broad ? patterns"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-170.md
sources: []
last_updated: 2026-03-25
---

## Summary
Follow-up to PR #169 (merged). After merge, Cursor Bugbot flagged a High Severity issue:
the `\?\s*$/m` regex in `detectActivity()` matched ANY line ending with `?`,
not just standalone `?` prompts — causing false `waiting_input` signals for error
messages and thinking output like "Missing module — did you install it?".

## Metadata
- **PR**: #170
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +16/-5 in 2 files
- **Labels**: none

## Connections
