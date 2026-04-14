---
title: "jleechanclaw-regression-detector"
type: source
tags: [jleechanclaw, regression, testing]
date: 2026-04-14
source_file: jleechanclaw/src/orchestration/regression_detector.py
---

## Summary
Regression detection for PR changes. Compares new changes against historical patterns to detect potential regressions. Uses prior review decisions and action outcomes to identify when new PRs might introduce similar issues to past failures.

## Key Claims
- Scans action_log.jsonl for prior failure patterns
- Compares PR characteristics against historical regressions
- Used as part of the review gate before merge readiness

## Connections
- [[jleechanclaw-pr-review-decision]] — related to PR quality gates

## Contradictions
- None identified