---
title: "WorldArchitect.AI CLAUDE.md — Primary Operating Protocol"
type: source
tags: [worldarchitect, claude-code, rules, protocol, ai-collaboration]
date: 2026-04-06
source_file: /Users/jleechan/worldarchitect.ai/CLAUDE.md
---

## Summary

The WorldArchitect.AI CLAUDE.md is the primary rules document governing AI-agent collaboration on the project. It mandates a mandatory greeting protocol ("Genesis Coder, Prime Mover,"), requires running a git-header script on every response, enforces strict test-driven development (all CI failures block merges), and requires full autonomous execution chains (test locally → test on GCP preview → commit → push → notify). It bans several anti-patterns including keyword intent detection, synthetic data generation, and stripping tool definitions.

## Key Claims

- Claude Code CLI is a terminal agent, NOT Desktop — it can run servers, execute commands, and test services directly
- LLM decides, server executes — full context must be provided to LLM for decision-making
- Banned patterns: keyword/substring intent detection (use FastEmbed classifier), synthetic/fake data generation, stripping tool definitions, disabled-by-default flags
- Integration hierarchy for new files: existing file → utility → `__init__.py` → test → config → NEW (last resort)
- Python placement: `mvp_site/`, Scripts: `scripts/`, Tests: `mvp_site/tests/`
- Never delete unrelated content from origin/main; Integration > Modification > Deletion
- All failing CI tests are blockers — never merge with failing CI
- `/pr` must create actual PR with working URL, never give manual steps
- Evidence path: `/tmp/worldarchitect.ai/<branch>/<test_name>/latest/`
- Default: execute fully without asking; test → commit → push → notify automatically
- Timeout: 10 minutes / 600 seconds across all layers
- Testing with real services only (no mock mode) for `testing_mcp/` and `testing_ui/`

## Key Quotes

> "**Every response must begin with:** `Genesis Coder, Prime Mover,`" — mandatory greeting protocol

> "**BANNED Anti-Patterns**: Keyword/substring matching for intent (use FastEmbed classifier, <50ms)" — zero-tolerance on heuristic routing

> "**Fallback/synthetic data generation** — Never generate fake data to mask LLM failures. Fix prompts instead." — core quality principle

> "**Default: execute fully, don't ask.** The user rarely wants commands to run manually." — autonomy philosophy

> "NEVER merge PRs without explicit 'MERGE APPROVED' from user" — merge gate

## Connections

- [[Claude]] — this CLAUDE.md extends Claude Code CLI conventions
- [[ClaudeCode]] — governs Claude Code CLI behavior in the project
- [[Beads]] — uses beads for issue tracking in PR workflows
- [[TestingInfrastructure]] — testing_mcp and testing_ui run only against real services

## Contradictions

- None identified
