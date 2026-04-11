---
title: "PR #10: fix: preserve system_prompt context with SYSTEM_INSTRUCTION + transport capture fallback"
type: source
tags: []
date: 2026-02-22
source_file: raw/prs-worldai_claw/pr-10.md
sources: []
last_updated: 2026-02-22
---

## Summary
- **P0 bug fix — system instruction stack now preserved**: The session/system prompt stack sent to the LLM now combines canonical `SYSTEM_INSTRUCTION` with stored `session.system_prompt` when present, so custom campaign/session setup is still honored without losing the 9-layer GM guardrails.
- **Budget accounting aligned to actual prompt stack**: `enforceBudget()` now receives the same combined system prompt string used for the LLM call on both POST and GET turn routes.
- **Transport capture bac

## Metadata
- **PR**: #10
- **Merged**: 2026-02-22
- **Author**: jleechan2015
- **Stats**: +821/-87 in 18 files
- **Labels**: none

## Connections
