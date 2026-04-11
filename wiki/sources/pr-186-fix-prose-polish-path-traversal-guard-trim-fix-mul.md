---
title: "PR #186: fix(prose-polish): path traversal guard, trim fix, multi-fix dedup, hyphen Not-X"
type: source
tags: []
date: 2026-03-25
source_file: raw/prs-worldai_claw/pr-186.md
sources: []
last_updated: 2026-03-25
---

## Summary
Follow-up to PR #183, addressing remaining CodeRabbit review comments:

- **Critical**: Add `safePath()` guard to prevent path traversal in `prose_polish_scan` and `prose_polish_fix` tools — rejects relative paths and `..` sequences
- **Major**: Remove `trim()` in `fixLine()` to preserve Markdown indentation and whitespace
- **Major**: Deduplicate by line index before applying fixes (once-per-line) to prevent double-correction
- **Major**: Support hyphenated `Not-X` forms in `detectNotXRepetitio

## Metadata
- **PR**: #186
- **Merged**: 2026-03-25
- **Author**: jleechan2015
- **Stats**: +23/-8 in 3 files
- **Labels**: none

## Connections
