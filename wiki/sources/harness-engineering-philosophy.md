---
title: "Harness Engineering Philosophy"
type: source
tags: ["harness", "agent-orchestration", "openclaw", "ao", "infrastructure", "feedback-loops"]
date: 2026-04-07
source_file: "raw/harness-engineering-philosophy.md"
sources: []
last_updated: 2026-04-07
---

## Summary
This document defines harness engineering as the discipline of building environments, constraints, and feedback loops that enable AI agents to do reliable work. It describes a 4-layer architecture: agent environment (config-first), deterministic feedback loops (agent-orchestrator), LLM judgment (OpenClaw), and entropy management.

## Key Claims
- **Harness definition**: A harness is not a codebase agents work on, but the environment, constraints, and feedback loops that enable reliable agent work
- **4-layer architecture**: Agent Environment → Deterministic Feedback → LLM Judgment → Entropy Management
- **Documentation as infrastructure**: CLAUDE.md, AGENTS.md, SOUL.md are not docs but infrastructure read by agents on every turn
- **Deterministic first**: Don't use LLM when a rule will do; LLM only for the 20% requiring judgment
- **Fresh context**: Each headless call gets clean prompt with all context injected upfront, no accumulated context
- **Rippable harnesses**: Orchestration layer should be thin and replaceable, survive model updates

## Key Quotes
> "The discipline of building systems that make AI agents actually work." — OpenAI, February 2026

> "From the agent's perspective, anything it can't access in-context doesn't exist."

> "If you over-engineer the control flow, the next model update will break your system."

## Connections
- [[OpenClaw]] — runtime environment providing memory, tools, and persistent context
- [[Agent Orchestrator]] — deterministic reaction engine for predictable events
- [[OpenAI]] — source of the harness engineering concept
- [[Deterministic Feedback Loops]] — the reaction engine layer
- [[Entropy Management]] — self-improving prompts, autonomous PR review, convergence intelligence

## Contradictions
- []
