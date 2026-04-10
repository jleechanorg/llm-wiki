---
title: "Fail-Closed Error Handling"
type: concept
tags: [error-handling, fail-closed, orchestration, ci]
sources: [orchestration-system-design-justification.md]
last_updated: 2026-04-07
---

An error handling policy where failures propagate upward and block operations rather than returning empty or default values. In `gh_integration.py`: CI check failures propagate (never silently return empty), unknown states map to "failed", GraphQL errors block merges.

Contrast with fail-open: returning empty results that would allow merging despite failures.

See: [[gh_integration.py]], [[MergeReadiness]]
