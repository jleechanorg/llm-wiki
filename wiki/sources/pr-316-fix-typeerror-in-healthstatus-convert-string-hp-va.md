---
title: "PR #316: Fix TypeError in HealthStatus: Convert string HP values to integers"
type: source
tags: []
date: 2025-07-06
source_file: raw/prs-worldarchitect-ai/pr-316.md
sources: []
last_updated: 2025-07-06
---

## Summary
This PR fixes a TypeError that occurs when Firestore returns HP values as strings instead of integers, causing the comparison `hp < 0` in HealthStatus to fail.

## Metadata
- **PR**: #316
- **Merged**: 2025-07-06
- **Author**: jleechan2015
- **Stats**: +372/-7 in 6 files
- **Labels**: none

## Connections
