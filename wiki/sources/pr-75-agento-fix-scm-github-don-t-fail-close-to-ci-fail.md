---
title: "PR #75: [agento] fix(scm-github): don't fail-close to CI failing on GraphQL rate limit errors"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-75.md
sources: []
last_updated: 2026-03-21
---

## Summary
When GitHub GraphQL rate limits are exhausted (common when multiple AO agents are running simultaneously), `getCISummary` was catching the error and fail-closing to `"failing"`, and `getReviewDecision` was throwing uncaught. The lifecycle poller then fired `ci-failed` and `changes-requested` reactions on every poll cycle, spamming agents with \"CI is failing on your PR\" when the real issue was a transient rate limit.

Observed in session jcc-13: agent correctly assessed PR #319 as green via RES

## Metadata
- **PR**: #75
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +136/-49 in 2 files
- **Labels**: none

## Connections
