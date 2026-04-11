---
title: "PR #334: [agento] fix(gemini): pass through Gemini-native model IDs + add missing CLI deps"
type: source
tags: []
date: 2026-04-02
source_file: raw/prs-worldai_claw/pr-334.md
sources: []
last_updated: 2026-04-02
---

## Summary
`ao spawn --agent gemini` failed with "Agent plugin 'gemini' not found" when using the globally installed `ao` binary, and the gemini plugin unconditionally stripped `--model` flags, preventing Gemini-native model IDs like `gemini-3-flash-preview` from being passed through.

## Metadata
- **PR**: #334
- **Merged**: 2026-04-02
- **Author**: jleechan2015
- **Stats**: +84/-13 in 7 files
- **Labels**: none

## Connections
