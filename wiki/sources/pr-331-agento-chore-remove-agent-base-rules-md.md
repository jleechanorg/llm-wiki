---
title: "PR #331: [agento] chore: remove AGENT_BASE_RULES.md"
type: source
tags: []
date: 2026-03-21
source_file: raw/prs-worldai_claw/pr-331.md
sources: []
last_updated: 2026-03-21
---

## Summary
`workspace/AGENT_BASE_RULES.md` was used as a shared rules file injected into AO agent sessions via `agentRulesFile:` in `agent-orchestrator.yaml`. As part of a config consolidation, its unique content (pre-exit checklist, MCP mail inbox polling protocol, when-stuck escalation steps) was merged into `defaults.agentRules` and the `agentRulesFile:` references were removed from all projects.

## Metadata
- **PR**: #331
- **Merged**: 2026-03-21
- **Author**: jleechan2015
- **Stats**: +0/-94 in 1 files
- **Labels**: none

## Connections
