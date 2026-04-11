---
title: "fix(green-gate): use --paginate for Gate 3 CR review check"
type: source
tags: [worldarchitect.ai, ci, green-gate, github-api, reviews, pagination]
date: 2026-04-11
source_file: raw/worldarchitect.ai/pr-930ed371d6.md
---

## Summary
Fixes Gate 3 review check that failed on PRs with many reviews. Without `--paginate`, the reviews API only returns the first page. For PRs with many reviews, the most recent APPROVED review may be on a later page — causing Gate 3 to see a stale DISMISSED state as the "latest" and fail incorrectly.

## Key Fix
- Drop `--jq` flag (incompatible with `--paginate` for cross-page logic)
- Pipe all pages to external jq using `-rs 'add | ...'` pattern
- Matches how `skeptic-cron.yml` reads reviews

## Changed Files
- `.github/workflows/green-gate.yml`: +8/-8 lines

## Connections
- [[green-gate]] — CI workflow this fixes
- Related: `c4e308a94a` (treat CR=DISMISSED as Gate 3 pass)

## Bug Pattern
gh CLI pagination edge case: `--jq` and `--paginate` are incompatible. When needing to aggregate across all pages, use `-rs 'add | ...'` jq piping pattern.
