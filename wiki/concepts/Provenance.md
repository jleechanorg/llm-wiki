---
title: "Provenance"
type: concept
tags: [testing, traceability, git]
sources: []
last_updated: 2026-04-08
---

Provenance in testing refers to metadata that traces the origin of test results, typically including git commit hash (HEAD), branch name, and timestamp. Used for reproducing and verifying test conditions.

## Key Fields
- **git_head**: Full git commit SHA
- **git_branch**: Current branch name
- Often captured via capture_provenance() function

## Related
- [[EvidenceUtils]] provides capture_provenance and validate_provenance functions
