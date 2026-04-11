---
title: "PR #428: [agento] fix(skeptic): LLM fallback chain codex→claude→gemini"
type: source
tags: []
date: 2026-04-11
source_file: raw/prs-worldai_claw/pr-428.md
sources: []
last_updated: 2026-04-11
---

## Summary
- **Bug**: When Codex CLI fails with ENOBUFS/spawnSync errors, skeptic returns VERDICT: FAIL which permanently blocks the PR gate. Observed in worldarchitect.ai PR #6161.
- **Fix**: Add a 3-model fallback chain (codex, claude, gemini). Only infrastructure failures trigger fallback; legitimate verdicts (even FAIL) are accepted immediately.
- **Key change**: When ALL models fail with infra errors, returns VERDICT: SKIPPED (not FAIL) so the gate does not permanently block PRs.

## Metadata
- **PR**: #428
- **Merged**: 2026-04-11
- **Author**: jleechan2015
- **Stats**: +352/-102 in 4 files
- **Labels**: none

## Connections
