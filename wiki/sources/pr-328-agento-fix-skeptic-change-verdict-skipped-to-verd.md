---
title: "PR #328: [agento] fix(skeptic): change VERDICT: SKIPPED to VERDICT: FAIL (fail-closed)"
type: source
tags: []
date: 2026-03-31
source_file: raw/prs-worldai_claw/pr-328.md
sources: []
last_updated: 2026-03-31
---

## Summary
- Change `VERDICT: SKIPPED` → `VERDICT: FAIL` in `llmEval()` in `packages/cli/src/lib/llm-eval.ts` (5 places)
- Add `--dangerously-skip-permissions --no-input` to `tryClaudePrint()` for non-interactive headless eval
- Remove SKIPPED detection from `skeptic-cron.yml` gate check (infra failures now emit FAIL, not SKIPPED)
- `claim-verifier.ts`: `checkRunLevel()` and `checkCommentLevel()` now return `fail` (not `absent`) for SKIPPED verdicts — fail-closed

## Metadata
- **PR**: #328
- **Merged**: 2026-03-31
- **Author**: jleechan2015
- **Stats**: +62/-54 in 6 files
- **Labels**: none

## Connections
