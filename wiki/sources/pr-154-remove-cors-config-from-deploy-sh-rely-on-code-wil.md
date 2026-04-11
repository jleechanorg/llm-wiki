---
title: "PR #154: Remove CORS config from deploy.sh, rely on code wildcard"
type: source
tags: []
date: 2025-10-04
source_file: raw/prs-/pr-154.md
sources: []
last_updated: 2025-10-04
---

## Summary
- Removed redundant CORS_ALLOWED_ORIGINS environment variable from deploy.sh
- Code already has wildcard CORS configuration in server.ts that handles all deployed frontends

## Metadata
- **PR**: #154
- **Merged**: 2025-10-04
- **Author**: jleechan2015
- **Stats**: +18/-19 in 2 files
- **Labels**: none

## Connections
