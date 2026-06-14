---
title: "Beads No-Auto-Flush Stops JSONL Churn (PR #7270)"
type: source
tags: ["beads", "jsonl", "no-auto-flush", "pr-7270", "feedback"]
date: 2026-06-05
source_file: feedback_2026-06-05_beads_no_auto_flush_stops_jsonl_churn.md
---

## Summary
The fix for 1663/1663 .beads/issues.jsonl reorder churn is `no-auto-flush: true` in `.beads/config.yaml`. Landed on main via PR #7270 (`380f1b5ee4`, 2026-06-04).

## Key Claims
- Giant issues.jsonl diffs (1663 insertions / 1663 deletions = pure reorder/reformat) from `br` auto-flushing on every command
- Fix (durable): `no-auto-flush: true` in `.beads/config.yaml`
- DB is source of truth locally; under no-auto-flush, beads.db and issues.jsonl can diverge without churn

## Key Quotes
> Syncing a feature branch with main (merge) brings the fix in permanently

## Connections
- [[Beads]] — issue tracking
