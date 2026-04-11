---
title: "PR #46: fix(mc): remove keyword-based CLI routing from TaskPoller"
type: source
tags: []
date: 2026-03-05
source_file: raw/prs-worldai_claw/pr-46.md
sources: []
last_updated: 2026-03-05
---

## Summary
- Remove all keyword-based CLI routing from TaskPoller (`detect_cli()`, `DEFAULT_CLI_KEYWORDS`, prompt library, `build_claudem_dispatch()`, multi-CLI subprocess dispatch)
- TaskPoller now delegates entirely to `ai_orch run` which handles CLI selection, model choice, and claudem/minimax internally
- Removes the banned anti-pattern (keyword-based intent detection to bypass LLM judgment) per CLAUDE.md
- Net deletion: ~760 lines of routing/dispatch logic

## Metadata
- **PR**: #46
- **Merged**: 2026-03-05
- **Author**: jleechan2015
- **Stats**: +366/-967 in 4 files
- **Labels**: none

## Connections
