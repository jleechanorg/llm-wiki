---
title: "PR #701: Fix admin fallback rate limiting"
type: source
tags: [codex]
date: 2025-11-13
source_file: raw/prs-/pr-701.md
sources: []
last_updated: 2025-11-13
---

## Summary
- make the rate-limit contact email configurable via RATE_LIMIT_CONTACT_EMAIL so the backend and shared limiter stay in sync
- update the RateLimitTool to always include the contact/admin fallback emails (and optional overrides) when building the admin allowlist
- add regression coverage proving fallback admins do not inherit the 10/hr non-VIP throttle

## Metadata
- **PR**: #701
- **Merged**: 2025-11-13
- **Author**: jleechan2015
- **Stats**: +137/-4 in 3 files
- **Labels**: codex

## Connections
