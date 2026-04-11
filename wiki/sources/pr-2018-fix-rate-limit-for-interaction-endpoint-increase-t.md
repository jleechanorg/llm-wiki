---
title: "PR #2018: Fix rate limit for interaction endpoint - increase to 30000/hour"
type: source
tags: []
date: 2025-11-14
source_file: raw/prs-worldarchitect-ai/pr-2018.md
sources: []
last_updated: 2025-11-14
---

## Summary
- Fixes rate limit errors (429) on interaction endpoint that were blocking legitimate users
- Increases rate limit from 30/hour to 30000/hour (1000x increase)
- Per minute limit increased from 5 to 1000 per minute (200x increase)

## Metadata
- **PR**: #2018
- **Merged**: 2025-11-14
- **Author**: jleechan2015
- **Stats**: +9/-5 in 1 files
- **Labels**: none

## Connections
