---
title: "PR #257: docs(roadmap): evidence review schema — two-stage verification pipeline"
type: source
tags: []
date: 2026-03-17
source_file: raw/prs-worldai_claw/pr-257.md
sources: []
last_updated: 2026-03-17
---

## Summary
- Design doc for replacing comment-based evidence gate with git-tracked evidence bundles
- Two-stage pipeline: agent self-review then independent LLM verification
- Standard schema: `docs/evidence/{repo}/PR-{N}/{YYYYMMDD}_{HHMM}_pst/`
- Merge gate reads `verdict.json` (requires independent reviewer sign-off)

## Metadata
- **PR**: #257
- **Merged**: 2026-03-17
- **Author**: jleechan2015
- **Stats**: +231/-0 in 2 files
- **Labels**: none

## Connections
