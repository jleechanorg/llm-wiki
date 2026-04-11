---
title: "PR #142: fix: allow Cloud Run preview domains for CORS"
type: source
tags: [codex]
date: 2025-10-02
source_file: raw/prs-/pr-142.md
sources: []
last_updated: 2025-10-02
---

## Summary
- ensure the backend always whitelists Cloud Run PR preview frontends in its CORS configuration
- cover the preview domains in the CORS utility tests and improve null-origin handling
- fix the Jest configuration so ES module path mappings work during the tests
- add regression coverage for literal `"null"` origins when toggling `allowNullOrigin`

## Metadata
- **PR**: #142
- **Merged**: 2025-10-02
- **Author**: jleechan2015
- **Stats**: +66/-2 in 4 files
- **Labels**: codex

## Connections
