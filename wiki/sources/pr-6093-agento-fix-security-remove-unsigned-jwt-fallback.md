---
title: "PR #6093: [agento] fix(security): remove unsigned JWT fallback on expired tokens"
type: source
tags: []
date: 2026-04-04
source_file: raw/prs-worldarchitect-ai/pr-6093.md
sources: []
last_updated: 2026-04-04
---

## Summary
- Removes the vulnerable unsigned JWT fallback at main.py:1610-1645
- Attackers could forge any user_id by crafting JWTs with valid structure but garbage signatures
- The check 'exp' in error_str.lower() was too broad (matched 'exception', 'expected', etc.)
- Added 3 security tests to prevent regression

## Metadata
- **PR**: #6093
- **Merged**: 2026-04-04
- **Author**: jleechan2015
- **Stats**: +138/-55 in 2 files
- **Labels**: none

## Connections
