---
title: "PR #49: fix(scm-github): GraphQL-first with REST API fallback for rate limit resilience"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-49.md
sources: []
last_updated: 2026-03-21
---

## Summary
GitHub GraphQL rate limit (5000/hr) was being exhausted by the lifecycle manager polling ~269 sessions every 30s with ~5 GraphQL calls each (161k calls/hr). REST API has a separate 5000/hr budget that was untouched.

## Metadata
- **PR**: #49
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +565/-173 in 35 files
- **Labels**: none

## Connections
