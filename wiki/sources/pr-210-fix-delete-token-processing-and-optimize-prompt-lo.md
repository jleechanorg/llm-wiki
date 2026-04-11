---
title: "PR #210: Fix DELETE token processing and optimize prompt loading order"
type: source
tags: []
date: 2025-07-02
source_file: raw/prs-worldarchitect-ai/pr-210.md
sources: []
last_updated: 2025-07-02
---

## Summary
Fixes 2 of the 4 remaining issues from PR #189's comprehensive prompt cleanup.

### 1. DELETE Token Processing ✅
**Bug**: `__DELETE__` token only worked when the existing value was a dictionary  
**Fix**: Moved DELETE token handling to Case 1 (highest priority) to handle all value types

### 2. Loading Order Optimizations ✅
**Changes**:
- Moved `destiny_ruleset` from position 8 to position 4 (right after entity_schema)
- Added calibration conditional loading (was previously filtered out)

## Metadata
- **PR**: #210
- **Merged**: 2025-07-02
- **Author**: jleechan2015
- **Stats**: +392/-28 in 5 files
- **Labels**: none

## Connections
