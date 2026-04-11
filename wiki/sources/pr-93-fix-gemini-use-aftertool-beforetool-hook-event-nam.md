---
title: "PR #93: fix(gemini): use AfterTool/BeforeTool hook event names and write hooks before launch (orch-xmg5)"
type: source
tags: []
date: 2026-03-23
source_file: raw/prs-worldai_claw/pr-93.md
sources: []
last_updated: 2026-03-23
---

## Summary
Gemini sessions were spawning idle and never tracking their work in AO. Two root causes identified:

1. **Wrong hook event names**: AO wrote `PostToolUse`/`PreToolUse` to `.gemini/settings.json`, but Gemini CLI only recognizes `AfterTool`/`BeforeTool` (confirmed via `gemini hooks migrate` source). These keys are silently ignored, so `metadata-updater.sh` never runs.

2. **Wrong timing**: `postLaunchSetup` wrote the hooks AFTER Gemini launched. Gemini reads `settings.json` only at startup (confir

## Metadata
- **PR**: #93
- **Merged**: 2026-03-23
- **Author**: jleechan2015
- **Stats**: +336/-28 in 5 files
- **Labels**: none

## Connections
