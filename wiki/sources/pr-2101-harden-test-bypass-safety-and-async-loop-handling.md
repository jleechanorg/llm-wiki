---
title: "PR #2101: Harden test bypass safety and async loop handling"
type: source
tags: [codex]
date: 2025-11-24
source_file: raw/prs-worldarchitect-ai/pr-2101.md
sources: []
last_updated: 2025-11-24
---

## Summary
- Gate test auth bypass behind explicit environment flags, log usage, and narrow CORS exposure to test-only headers
- Replace per-request event-loop creation with a shared background loop and rate-limit using ProxyFix-sanitized client IPs
- Tighten local tooling by matching exact backend process patterns, validating local Firebase creds, and cleaning import validator allowlists

## Metadata
- **PR**: #2101
- **Merged**: 2025-11-24
- **Author**: jleechan2015
- **Stats**: +62/-34 in 3 files
- **Labels**: codex

## Connections
