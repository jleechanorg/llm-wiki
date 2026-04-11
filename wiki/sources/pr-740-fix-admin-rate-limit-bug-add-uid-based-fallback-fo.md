---
title: "PR #740: fix: Admin rate limit bug - add UID-based fallback for missing email claims in Firebase tokens"
type: source
tags: []
date: 2025-11-17
source_file: raw/prs-/pr-740.md
sources: []
last_updated: 2025-11-17
---

## Summary
Fixes critical production bug where admin user `jleechan@gmail.com` is incorrectly rate limited at **5 requests/hour** (anonymous limit) instead of **1000 requests/hour** (admin limit).

**Impact:** Production blocker - admin cannot use the system due to aggressive rate limiting.

## Metadata
- **PR**: #740
- **Merged**: 2025-11-17
- **Author**: jleechan2015
- **Stats**: +2367/-171 in 29 files
- **Labels**: none

## Connections
