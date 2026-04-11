---
title: "PR #211: Wire auto_resolve_threads into escalation flow"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-211.md
sources: []
last_updated: 2026-03-16
---

## Summary
This PR wires the  function into the escalation flow to resolve stale review threads after fix pushes and merges.

### Changes

1. **escalation_router.py**:
   - Add  field to  dataclass
   - Extract  from  when creating  for ci-failed and changes-requested events

2. **action_executor.py**:
   - Import  from  module
   - Add  helper to extract owner/repo/pr_number from PR URL
   - Add  helper to call resolve function when PR URL is available
   - Call  after  execution (when  is provided)
   -

## Metadata
- **PR**: #211
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +270/-0 in 3 files
- **Labels**: none

## Connections
