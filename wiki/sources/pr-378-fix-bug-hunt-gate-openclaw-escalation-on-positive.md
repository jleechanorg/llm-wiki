---
title: "PR #378: fix(bug-hunt): gate @openclaw escalation on positive bug count (#242)"
type: source
tags: []
date: 2026-03-24
source_file: raw/prs-worldai_claw/pr-378.md
sources: []
last_updated: 2026-03-24
---

## Summary
- Aligns daily bug-hunt notifications with [issue #242](https://github.com/jleechanorg/jleechanclaw/issues/242): do not append `@openclaw Please fix these bugs using agento` unless at least one bug is counted.
- Makes per-agent JSON parsing accept a top-level array or a `findings` array inside an object (common LLM output shape).
- Ignores non-numeric jq output when summing counts so arithmetic stays safe.

## Metadata
- **PR**: #378
- **Merged**: 2026-03-24
- **Author**: jleechan2015
- **Stats**: +20/-4 in 1 files
- **Labels**: none

## Connections
