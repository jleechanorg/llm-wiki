---
title: "PR #193: [agento] fix(prose-polish): address CR follow-up review comments"
type: source
tags: []
date: 2026-03-26
source_file: raw/prs-worldai_claw/pr-193.md
sources: []
last_updated: 2026-03-26
---

## Summary
Second follow-up to PR #183 / #186, addressing remaining review comments on the prose-polish plugin:

- **safePath** (mcp-tools.ts): Support workspace-relative paths (README.md, ./docs/ch1.md) by resolving them via `path.resolve()`; use `node:path.isAbsolute`/`normalize` for segment-level `..` traversal check instead of substring rejection; Windows absolute paths (C:\) now work
- **fixLine** (fixer.ts): Preserve leading indentation by extracting/restoring leading whitespace; collapse only intern

## Metadata
- **PR**: #193
- **Merged**: 2026-03-26
- **Author**: jleechan2015
- **Stats**: +147/-29 in 4 files
- **Labels**: none

## Connections
