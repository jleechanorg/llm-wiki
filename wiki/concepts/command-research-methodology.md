---
title: "Command Research Methodology"
type: concept
tags: [methodology, telemetry, metrics, data-mining, anti-noise]
---

# Command Research Methodology

## Definition
The empirical protocol for auditing and ranking slash command and skill usage across multi-platform AI developer environments (Hermes, Claude Code, Codex).

## Core Principles

### 1. The Anti-Noise Filter
Standard text search or `content.count("command")` across session transcripts is completely invalid because LLM runtime harnesses inject the full command/skill catalog in system reminders after intermediate tool turns. 

**Enforcement:**
- Match only exact prompt-start boundaries `(?:^|\s)/cmd` or canonical Claude `<command-name>/cmd</command-name>` XML tags.
- Filter against `PATH_PREFIXES` (`/Users`, `/tmp`, `/dev`, `/api`, `/src`, `/tests`, `/var`, `/home`, etc.) and `FILE_SUFFIXES` (`.py`, `.md`, `.ts`, `.sh`, `.json`).
- Strip automated system injections (`<skill_listing>`, `<EXTREMELY_IMPORTANT>`, `"Base directory for this skill:"`).

### 2. Dual-Taxonomy Invariant
Raw invocation counts without author attribution fail to differentiate between developer preferences and agent infrastructure. Every event must be classified into:
- **Human-Typed**: Role `user`, source `slack`/`cli`/`telegram`, non-bot author ID, promptSource `typed`/interactive, non-sidechain session.
- **Agentic / Subagent**: Delegated subagent sessions (`isSidechain: true`), Stop-hook iteration loops, cron dispatchers, and async worker lanes.

## Tooling Implementation
- **Canonical Skill**: `~/.claude/skills/command-research/SKILL.md`
- **Scanner Engine**: `~/.claude/skills/command-research/scripts/count_command_usage_unified.py`
- **Slash Command**: `/command-research [--days N] [--top N] [--human-only] [--agent-only] [--json]`

## Related Concepts
- [[EvidenceStandards]]
- [[EvidenceReview]]
- [[SystemPromptCapture]]
