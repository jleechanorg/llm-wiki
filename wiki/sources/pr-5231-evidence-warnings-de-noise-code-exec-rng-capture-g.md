---
title: "PR #5231: Evidence warnings: de-noise code_exec RNG + capture Gemini parts"
type: source
tags: []
date: 2026-02-10
source_file: raw/prs-worldarchitect-ai/pr-5231.md
sources: []
last_updated: 2026-02-10
---

## Summary
Reduces noise from evidence-bundle warning signals and improves evidence fidelity:
- `CODE_EXEC_NO_RNG` is now informational (no fabricated-dice wording); dice integrity remains enforced via existing dice-integrity checks.
- `action_resolution.mechanics.outcome` is treated as optional (canonical outcome remains `action_resolution.narrative_outcome`).
- LLM evidence capture now persists full Gemini `candidates.content.parts` (including non-text parts like executable_code / code_execution_result)

## Metadata
- **PR**: #5231
- **Merged**: 2026-02-10
- **Author**: jleechan2015
- **Stats**: +433/-566 in 21 files
- **Labels**: none

## Connections
