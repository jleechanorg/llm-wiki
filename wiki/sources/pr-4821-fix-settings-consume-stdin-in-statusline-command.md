---
title: "PR #4821: fix(settings): consume stdin in statusLine command"
type: source
tags: []
date: 2026-02-04
source_file: raw/prs-worldarchitect-ai/pr-4821.md
sources: []
last_updated: 2026-02-04
---

## Summary
Applies the stdin consumption fix identified in jleechanorg/claude-commands#231 review.

**Change:** Add `cat >/dev/null;` at the beginning of the statusLine bash command to consume any stdin that might be passed, preventing potential issues when the command is called in contexts with unexpected input data.

## Metadata
- **PR**: #4821
- **Merged**: 2026-02-04
- **Author**: jleechan2015
- **Stats**: +1/-1 in 1 files
- **Labels**: none

## Connections
