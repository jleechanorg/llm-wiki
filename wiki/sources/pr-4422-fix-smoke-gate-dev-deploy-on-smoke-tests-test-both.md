---
title: "PR #4422: fix(smoke): Gate dev deploy on smoke tests + test both Cerebras & Gemini 3"
type: source
tags: []
date: 2026-02-01
source_file: raw/prs-worldarchitect-ai/pr-4422.md
sources: []
last_updated: 2026-02-01
---

## Summary
- Gate dev auto-deploy on MCP smoke test success
- Run smoke tests against BOTH Cerebras and Gemini 3 to catch provider-specific regressions
- Add provider-aware dice strategy (Gemini=code_execution, Cerebras=native_two_phase)
- Add fallback dice execution when code_execution doesn't produce dice rolls
- Update default Gemini model to `gemini-3-flash-preview`
- Improve smoke test debugging with retry logic and better dice validation

**Key themes:**
- Provider-specific dice strategies
- Fallback

## Metadata
- **PR**: #4422
- **Merged**: 2026-02-01
- **Author**: jleechan2015
- **Stats**: +256/-46 in 6 files
- **Labels**: none

## Connections
