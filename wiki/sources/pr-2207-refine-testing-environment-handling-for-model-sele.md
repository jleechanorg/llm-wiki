---
title: "PR #2207: Refine testing environment handling for model selection"
type: source
tags: [codex]
date: 2025-12-01
source_file: raw/prs-worldarchitect-ai/pr-2207.md
sources: []
last_updated: 2025-12-01
---

## Summary
- stop the TESTING environment flag from forcing the Gemini test model and instead rely on MOCK_SERVICES_MODE or an explicit FORCE_TEST_MODEL override
- add documentation for the new FORCE_TEST_MODEL flag so running servers with TESTING=true do not unexpectedly swap models
- expand centralized model selection tests to cover the updated override behavior and ensure TESTING alone uses normal model selection

## Metadata
- **PR**: #2207
- **Merged**: 2025-12-01
- **Author**: jleechan2015
- **Stats**: +55/-20 in 3 files
- **Labels**: codex

## Connections
