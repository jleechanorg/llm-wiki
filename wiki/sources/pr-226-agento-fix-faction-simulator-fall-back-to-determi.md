---
title: "PR #226: [agento] fix(faction_simulator): fall back to deterministic generation when LLM bootstrap schema parse fails"
type: source
tags: []
date: 2026-04-07
source_file: raw/prs-worldai_claw/pr-226.md
sources: []
last_updated: 2026-04-07
---

## Summary
- Wrap `factionBootstrapSchema.parse` in try-catch in `generateStructuredWorldBootstrap`
- On parse failure, fall back to `generateFactionsFromUniverseSeed` using the same bootstrap config
- Resolves 4 MCP + 12 HTTP test failures caused by Zod crash when LLM returns malformed JSON missing `factions` field

## Metadata
- **PR**: #226
- **Merged**: 2026-04-07
- **Author**: jleechan2015
- **Stats**: +62/-29 in 2 files
- **Labels**: none

## Connections
