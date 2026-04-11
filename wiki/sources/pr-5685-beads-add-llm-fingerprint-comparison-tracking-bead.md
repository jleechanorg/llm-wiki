---
title: "PR #5685: beads: add LLM fingerprint comparison tracking bead"
type: source
tags: []
date: 2026-02-21
source_file: raw/prs-worldarchitect-ai/pr-5685.md
sources: []
last_updated: 2026-02-21
---

## Summary
- Adds `.beads/REV-schema-llm-fingerprint.md` tracking the apples-to-oranges LLM trace comparison problem found during schema prompt regression testing
- Main branch tests only captured MCP proxy traffic (no direct Gemini calls); branch tests captured direct Gemini HTTP with full `systemInstruction` payloads
- Documents root cause: main ran without a valid `GEMINI_API_KEY` so it never reached Gemini; branch used BYOK from Firestore
- Recommends re-running main branch tests with a valid API key f

## Metadata
- **PR**: #5685
- **Merged**: 2026-02-21
- **Author**: jleechan2015
- **Stats**: +48/-0 in 1 files
- **Labels**: none

## Connections
