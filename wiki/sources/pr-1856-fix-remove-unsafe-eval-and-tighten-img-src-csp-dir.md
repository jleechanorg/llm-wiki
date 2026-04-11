---
title: "PR #1856: fix: Remove unsafe-eval and tighten img-src CSP directives"
type: source
tags: []
date: 2025-10-13
source_file: raw/prs-worldarchitect-ai/pr-1856.md
sources: []
last_updated: 2025-10-13
---

## Summary
Security hardening follow-up to PR #1855 based on unanimous AI reviewer feedback.

### Changes
1. **Removed `unsafe-eval` from script-src** ❌→✅
   - Not required for Bootstrap or Firebase functionality
   - Significantly weakens XSS protection by allowing dynamic code execution
   - Flagged by all 4 AI reviewers as P1 security vulnerability

2. **Tightened img-src from wildcard `https:`** 🔓→🔒
   - **Before**: Allow images from ANY HTTPS domain
   - **After**: Only allow specific trusted domains:

## Metadata
- **PR**: #1856
- **Merged**: 2025-10-13
- **Author**: jleechan2015
- **Stats**: +22/-10 in 1 files
- **Labels**: none

## Connections
