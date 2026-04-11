---
title: "PR #461: [agento] fix(doctor): silence expected warnings for nvm Node 22 and unconfigured Discord"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-461.md
sources: []
last_updated: 2026-03-31
---

## Summary
Two doctor.sh WARNs fire on every monitor cycle despite being expected, correct configuration:
1. WARN: channels.discord.token:missing/placeholder -- Discord is intentionally not configured
2. WARN: gateway service uses Node from a version manager -- CLAUDE.md mandates nvm Node 22; Homebrew Node 24 breaks native modules (better-sqlite3 ABI mismatch)

## Metadata
- **PR**: #461
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +83/-36 in 3 files
- **Labels**: none

## Connections
