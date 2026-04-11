---
title: "PR #6006: fix(cache): bead followups rev-ukw/834/oy0/ixu/9td2/n1fc/seg3 + streaming CE roadmap"
type: source
tags: []
date: 2026-03-18
source_file: raw/prs-worldarchitect-ai/pr-6006.md
sources: []
last_updated: 2026-03-18
---

## Summary
Post-PR-6003 bead followups — hardening cache management, tightening fallback logic, proactive TTL expiry, N-1 for first-ever caches, and provably-fair seed injection in streaming.

- **rev-ukw**: Parenthesize `and/or` in `create_cache()` for explicit precedence
- **rev-834**: Restrict PT011/B017 lint ignores to specific legacy test files (was global wildcard)
- **rev-oy0**: Narrow `reset_cache()` to actual cache errors; unknown errors re-raise (don't nuke valid caches for quota/safety/rate-limi

## Metadata
- **PR**: #6006
- **Merged**: 2026-03-18
- **Author**: jleechan2015
- **Stats**: +801/-304 in 11 files
- **Labels**: none

## Connections
