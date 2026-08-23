---
title: "Command Research Methodology & Top 20 Empirical Audit (2026-08-23)"
type: source
tags: [telemetry, commands, methodology, skills, hermes, claude-code, codex, empirical-audit]
date: 2026-08-23
source_file: "raw/command-research-methodology-and-top20-audit-2026-08-23.md"
---

## Summary
Empirical multi-store data mining across 128,756 session turns in Hermes SQLite (`~/.hermes/state.db`), Claude Code JSONL logs (`~/.claude/projects/`), and Codex SQLite (`~/.codex/state_5.sqlite`). Resolves the substring noise trap caused by system-reminder catalog dumps and establishes a clean separation between **Human-Typed Interactive Staples** and **Agentic/Subagent Autonomous Rails**.

## Key Claims
1. **Raw substring counts are invalid**: Claude Code injects the entire tool/skill catalog into system reminders on every turn, producing 10,000–180,000 false hits per command name.
2. **Exact token regex is required**: Invocations must match prompt-start tokens `(?:^|\s)/cmd` or canonical Claude Code `<command-name>/cmd</command-name>` tags with path and URL exclusions.
3. **Dual Taxonomy**:
   - Top Human-Typed: `/advice` (8,145), `/green` (4,090), `/repro` (2,954), `/research` (2,690, 66.7% human), `/ms` (2,586), `/history` (2,320).
   - Top Agentic: `/es` (19,475, 97.2% agentic), `/er` (18,273, 89.2% agentic), `/green` (13,625), `/smoke` (8,282, 98.4% agentic), `/execute` (7,136, 100% agentic).
4. **Tool Consolidation**: All prior art consolidated into unified scanner `~/.claude/skills/command-research/scripts/count_command_usage_unified.py` and canonical command `/command-research`.

## Connections
- [[CommandResearchMethodology]] — The codified multi-store empirical audit protocol
- [[EvidenceStandards]] — High-volume agentic proof construction rail (`/es`)
- [[EvidenceReview]] — High-volume agentic verification rail (`/er`)
- [[ConversationHistorySparse]] — Top human conversation recall staple (`/history`)
- [[MemorySearch]] — Multi-system memory retrieval (`/ms`)
- [[ClaudeCommandsRepo]] — The repository containing slash command definitions
