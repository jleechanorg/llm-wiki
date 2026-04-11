---
title: "The Five Harness Layers"
type: concept
tags: [agent-patterns, harness-engineering, architecture]
sources: []
last_updated: 2026-04-11
---

## Summary
A 5-layer model for the agent harness (the infrastructure surrounding the model) that maps responsibilities, rates of change, tooling, and ownership. Provides a shared vocabulary for diagnosing harness gaps and making build vs. buy decisions.

## The Five Layers

### Layer 1 — Constraint (Skeleton)
Deterministic structural rules enforced without any LLM involved. Enforces boundaries the agent cannot cross.

**Examples:** Module dependency rules, file structure conventions, naming conventions, custom linters (ESLint, Clippy), ArchUnit-style tests, OpenAPI contract enforcement.

- **Rate of change:** Slow
- **Owner:** Architecture / senior engineers
- **Leverage:** High — cheap, zero false positives, prevents entire failure categories

**Key insight:** On managed platforms (e.g. Anthropic Managed Agents), L1 offers the highest marginal return. Most teams over-invest in L4 (verification) while skipping L1 entirely.

### Layer 2 — Context (Memory)
Controls exactly what the model sees at the start of each turn.

**Examples:** CLAUDE.md/AGENTS.md files, progress/scratchpad files, curated architectural decision records, progressive disclosure documents.

- **Rate of change:** Medium
- **Owner:** Daily development team
- **Note:** Human-written, concise files work best. LLM-generated or bloated overviews often hurt performance.

### Layer 3 — Execution (Hands)
Manages available actions and guardrails for what the agent can actually do.

**Examples:** Tool orchestration, MCP servers, sub-agent dispatch, sandboxing, dynamic tool scoping, permission models.

- **Rate of change:** Medium
- **Owner:** Platform engineering

**Key insight:** Fewer tools = better results. Too many tools push the model into "the dumb zone" — a state where excessive options degrade performance.

### Layer 4 — Verification (Immune System)
Checks output correctness and safety before it affects the world.

**Examples:** Structured checks, pre-stop hooks, silent-on-success/loud-on-failure patterns, failure pattern encoding.

- **Rate of change:** Fast
- **Owner:** Shared (developers + QA)

**Key insight:** Often delivers the biggest reliability gains — teams report 2–3× quality improvements from verification layer investment alone.

### Layer 5 — Lifecycle (Nervous System)
Treats the agent as a production process with startup, shutdown, and continuous operation.

**Examples:** Health monitoring, crash recovery, cost tracking, human-in-the-loop escalation, session management.

- **Rate of change:** Slow
- **Owner:** SRE / DevOps

## Managed Platform Coverage (Anthropic Managed Agents, April 2026)

Anthropic's Managed Agents platform effectively provides Layers 2, 3, and 5 as managed infrastructure:
- Session durability and context handling (L2)
- Sandbox/tool orchestration (L3)
- Crash recovery, scaling, cost tracking, brain/hands decoupling (L5)

The **brain/hands/session decoupling** — where brain runs the harness loop calling Claude, hands are disposable sandboxes, and session is a durable event log — delivered major performance wins: ~60% p50 and >90% p95 reduction in time-to-first-token.

**Coverage gap:** Teams are still responsible for L1 (domain-specific architectural constraints) and L4 (acceptance criteria and verification). Most teams over-invest in partial L4 while skipping L1, which now offers the highest marginal return on managed platforms.

## Build vs. Buy Decision Framework

| Layer | Managed Platform | Self-Hosted |
|---|---|---|
| L1 Constraint | Build (highest ROI) | Build |
| L2 Context | Managed | Build |
| L3 Execution | Managed | Build |
| L4 Verification | Build | Often start here |
| L5 Lifecycle | Managed | Build |

## Diagnostic Questions (per layer)
1. Do we have something here?
2. Is it maintained?
3. Does it measurably help?

## When NOT to invest heavily
- Prototypes
- Single-shot tasks
- Legacy spaghetti codebases
- While still evaluating runtimes

## Success Case: OpenAI Codex
OpenAI's Codex success reportedly came from heavy emphasis on Layer 1 (constraints) — the rigorous enforcement of coding rules and file structure boundaries.

## Sources
- Mitchell Hashimoto (popularized "harness engineering" and "never make that mistake again" principle)
- OpenAI engineering (Codex L1 emphasis)
- LangChain
- HumanLayer
- Birgitta Böckeler
- Anthropic engineering posts

## Connections
- [[jeffrey-oracle]] — an L4 verification layer for the worldarchitect.ai project
- [[StructureDriftPattern]] — an L1 failure case: constraint layer didn't catch fields being incorrectly nested
