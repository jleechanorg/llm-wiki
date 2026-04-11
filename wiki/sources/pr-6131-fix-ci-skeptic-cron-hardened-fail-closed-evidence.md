---
title: "PR #6131: fix(ci): skeptic-cron hardened fail-closed evidence gate (Gate 6)"
type: source
tags: []
date: 2026-04-09
source_file: raw/prs-worldarchitect-ai/pr-6131.md
sources: []
last_updated: 2026-04-09
---

## Summary
- Hardens `skeptic-cron.yml` Gate 6 (evidence): fail-closed unless `evidence-review-bot` has **APPROVED** on the PR HEAD SHA, or Evidence Gate / Evidence Review check-runs all pass on that SHA.
- Restores the hardened merge-gate behavior for CodeRabbit parsing, Bugbot evaluation, `HEAD_SHA` fallback handling, and operator merge controls after rebasing onto `main`.
- Adds the per-PR design note at `docs/design/pr-designs/pr-6131.md`.
- Keeps the workflow YAML-safe by writing the evidence-request

## Metadata
- **PR**: #6131
- **Merged**: 2026-04-09
- **Author**: jleechan2015
- **Stats**: +262/-12 in 7 files
- **Labels**: none

## Connections
