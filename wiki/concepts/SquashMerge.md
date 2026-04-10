---
title: "Squash-Merge"
type: concept
tags: [git, merge-strategy, pull-request]
sources: []
last_updated: 2026-04-08
---

A Git merge strategy where all commits from a feature branch are squashed into a single commit when merging into the target branch. The commit message typically includes the PR reference in the format `Description (#123)`.

## Detection Challenge
Squash-merge detection in scripts must correctly identify PR references while avoiding false positives:
- Must require at least one digit: `(#123)` vs `(#)` or `(#abc)`
- Must handle edge cases like spaces: `(# 123)` should not match
- Must use fixed-strings mode to prevent regex interpretation

## Related
- [[integrate-sh]] — script implementing detection
- [[squash-merge-detection-tests]] — tests for the detection logic
