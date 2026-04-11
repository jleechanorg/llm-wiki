---
title: "PR #320: fix: refine GitHub remote sanitization"
type: source
tags: [codex]
date: 2025-10-13
source_file: raw/prs-/pr-320.md
sources: []
last_updated: 2025-10-13
---

## Summary
- strip query and fragment parts from git@ GitHub remotes before building the sanitized path
- ensure fallback sanitization enforces github.com host and rejects empty or malformed paths

## Metadata
- **PR**: #320
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +18/-2 in 1 files
- **Labels**: codex

## Connections
