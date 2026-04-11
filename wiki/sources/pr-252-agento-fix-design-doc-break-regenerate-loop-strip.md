---
title: "PR #252: [agento] fix(design-doc): break regenerate-loop + strip entity-encoded CURSOR_SUMMARY"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-252.md
sources: []
last_updated: 2026-03-28
---

## Summary
Issue #419: `scripts/generate-pr-design-docs.mjs` generates two bugs that cause a permanent regenerate-loop on any PR using the design-doc workflow:

1. **Entity-encoded CURSOR_SUMMARY comment leaking into descriptions** — the PR body may contain `\u003c!-- CURSOR_SUMMARY --\u003e` or `&lt;!-- CURSOR_SUMMARY --&gt;` (HTML-entity or unicode-escaped forms of the comment marker). `extractDescription` only stripped the plain `<!-- ... -->` form.
2. **Workflow uses stale PR-branch script** — the work

## Metadata
- **PR**: #252
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +204/-15 in 6 files
- **Labels**: none

## Connections
