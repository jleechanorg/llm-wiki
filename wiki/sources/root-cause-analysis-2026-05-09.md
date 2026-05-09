---
title: "Root Cause Analysis — Bug Fix PRs #6839-#6844"
type: source
tags: [root-cause, rca, worldarchitect, regression]
date: 2026-05-09
source_file: raw/root_cause_analysis_2026-05-09.md
---

## Summary

Git archaeology across 5 recent bug fix PRs traced each bug to its original breaking PR. Common patterns: architectural gaps at mode intersections (God Mode + Combat), strict validation severing legacy fallbacks, flawed dual-condition guards, silent event listener leaks, and duplicated constant lists causing merge-rebase drift.

## Key Claims

- PR #6844: Combat trap from architectural gap in PR #2553/#3020 (no God Mode cleanup path)
- PR #6843: Location fallback severed by PR #5563 strict schema validation
- PR #6842: AND-logic CC modal guard from PR #6225 never fires for templates
- PR #6841: .bind(this) leak migrated from PR #1082, existed from V1 day 1
- PR #6839: Duplicated cooldown lists from PR #6308 caused NameError after rebase

## Connections

- [[AdminOverrideContract]] — Trend A: admin overrides leave stale flags
- [[ModalIntersection]] — Trend B: concurrent modal systems corrupt state
- [[EventListenerMemoryLeak]] — Trend C: .bind(this) anti-pattern
- [[StaleFlag]] — Common symptom across 4/5 PRs
