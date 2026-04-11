---
title: "PR #6087: [agento] fix(skeptic-cron): convert null mergeable to string for GHA output"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6087.md
sources: []
last_updated: 2026-04-04
---

## Summary
- **Root cause**: `mergeable: null` for PRs with `mergeable_state=unknown` caused GitHub Actions to reject the workflow output (GHA only accepts strings/numbers, not bare `null`)
- **Symptom**: "Unable to process file command output" failure + "Invalid format" annotation on `skeptic-cron` run #23969907460
- **Fix**: Pipe `mergeable` through `jq`'s `tostring` so `null` becomes "null" (valid JSON string)

## Metadata
- **PR**: #6087
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +2/-2 in 1 files
- **Labels**: none

## Connections
