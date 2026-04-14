---
title: "jleechanclaw — Harness Engineering Philosophy"
type: source
tags: [jleechanclaw, harness-engineering, agent-orchestration, openclaw, feedback-loops]
date: 2026-04-14
source_file: jleechanclaw/docs/HARNESS_ENGINEERING.md
---

## Summary

Harness engineering is the discipline of building systems that make AI agents actually work. Rather than writing application code, harness engineers design environments, constraints, feedback loops, and intent specifications. This repo is itself a harness — not a codebase agents work on, but the environment, constraints, and feedback loops that enable agents to do reliable work across all jleechanorg projects.

## Key Claims

- **Layer 1: Agent Environment (config-first)** — SOUL.md, TOOLS.md, CLAUDE.md, AGENTS.md, openclaw.json, per-agent models.json, and skills/ directory provide the scaffolding agents read directly
- **Layer 2: Deterministic Feedback Loops (agent-orchestrator)** — ao provides deterministic reactions to predictable events: ci-failed, changes-requested, agent-stuck. No LLM needed for the predictable 80%
- **Layer 3: LLM Judgment (OpenClaw)** — OpenClaw handles the 20% that requires judgment — vague reviews, task decomposition, conflicting failures, strategy decisions
- **Layer 4: Entropy Management** — Harnesses degrade over time; planned responses include self-improving prompts (ORCH-04k), autonomous PR review (ORCH-apr), and convergence intelligence (ORCH-cil)
- **Reference:** [OpenAI: Harness Engineering](https://openai.com/index/harness-engineering/) (February 2026)

## Key Quotes

> "The discipline of building systems that make AI agents actually work."
> — OpenAI, February 2026

> "From the agent's perspective, anything not in context doesn't exist — so the harness must make everything accessible."

## Connections

- [[AgentOrchestrator]] — the reaction engine providing deterministic feedback
- [[OpenClaw]] — the LLM judgment layer above AO
- [[HarnessFailurePatterns]] — documented failure modes in harness engineering
- [[EntropyManagement]] — degradation patterns and countermeasures
- [[DRIVE_TO_7_GREEN_HARNESS_FAILURE_2026-04-08]] — specific harness failure analysis

## Contradictions

- Layer 3 (OpenClaw) is described as handling the 20% requiring judgment, but [[AO-Blocker-Matrix]] documents 7-green PR criteria that include automated checks — the boundary between "deterministic enough for AO" and "requires LLM judgment" remains blurry in practice
