---
title: "PR #646: fix: Rate limiting (10/20 req/hr/day) + CRITICAL: Fix ConversationAgent rate limit bypass"
type: source
tags: []
date: 2025-11-12
source_file: raw/prs-/pr-646.md
sources: []
last_updated: 2025-11-12
---

## Summary
**Primary Changes:**
1. Updated rate limits: Non-VIP users now limited to 10 req/hour and 20 req/day (was 15/30)
2. **CRITICAL SECURITY FIX:** ConversationAgent was bypassing rate limits entirely - now properly enforced

## Metadata
- **PR**: #646
- **Merged**: 2025-11-12
- **Author**: jleechan2015
- **Stats**: +8195/-1969 in 15 files
- **Labels**: none

## Connections
