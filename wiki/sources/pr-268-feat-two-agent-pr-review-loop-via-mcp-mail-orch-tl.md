---
title: "PR #268: feat: two-agent PR review loop via MCP mail (orch-tlkk)"
type: source
tags: []
date: 2026-03-18
source_file: raw/prs-worldai_claw/pr-268.md
sources: []
last_updated: 2026-03-18
---

## Summary
The Python evidence pipeline (PR #265: evidence_bundle.py + stage2_reviewer.py + verdict.json) works but is brittle — custom file formats, CLI dispatch fragility, no feedback loop. This PR replaces it with a reviewer agent that communicates with the coder via MCP mail and posts real GitHub PR reviews.

## Metadata
- **PR**: #268
- **Merged**: 2026-03-18
- **Author**: jleechan2015
- **Stats**: +785/-0 in 4 files
- **Labels**: none

## Connections
