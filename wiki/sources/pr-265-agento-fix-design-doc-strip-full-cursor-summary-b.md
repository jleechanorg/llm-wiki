---
title: "PR #265: [agento] fix(design-doc): strip full CURSOR_SUMMARY block — prevent orphan closing tags"
type: source
tags: []
date: 2026-03-29
source_file: raw/prs-worldai_claw/pr-265.md
sources: []
last_updated: 2026-03-29
---

## Summary
- Fix `extractDescription()` in `scripts/generate-pr-design-docs.mjs` to strip the **full** `CURSOR_SUMMARY` block (opening marker + content + closing marker) in one pass
- This prevents the closing tag from being orphaned as visible text in generated `.html` design docs
- Keep the fallback HTML comment stripper non-greedy per-comment using `[\s\S]*?` with global replacement

## Metadata
- **PR**: #265
- **Merged**: 2026-03-29
- **Author**: jleechan2015
- **Stats**: +160/-124 in 5 files
- **Labels**: none

## Connections
