---
title: "PR #258: [agento] refactor(skeptic-gate): route skeptic evaluation through AO worker instead of GHA API keys"
type: source
tags: []
date: 2026-03-28
source_file: raw/prs-worldai_claw/pr-258.md
sources: []
last_updated: 2026-03-28
---

## Summary
skeptic-gate.yml tried to install Codex/Claude CLI and run skeptic directly in GitHub Actions, requiring ANTHROPIC_API_KEY or OPENAI_API_KEY as repo secrets. Since those keys are not configured (and should not be), every PR gets VERDICT: SKIPPED, exit 0, false success. The entire 7-green enforcement system has been silently disabled.

The AO infrastructure for skeptic evaluation already exists (merged in PR #223, bd-skp2):
- skeptic-reviewer.ts calls ao skeptic verify
- fork-skeptic-extension.ts

## Metadata
- **PR**: #258
- **Merged**: 2026-03-28
- **Author**: jleechan2015
- **Stats**: +1148/-106 in 11 files
- **Labels**: none

## Connections
