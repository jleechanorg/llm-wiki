---
title: "Harness Engineering"
type: concept
tags: ["harness", "agent", "infrastructure", "philosophy", "AI-engineering", "documentation", "context-management"]
sources: ["harness-engineering-philosophy", "openclaw-workshop-notes", "openai-harness-ryan-notes"]
last_updated: 2026-04-08
---

Harness engineering is the discipline of building systems that make AI agents actually work. A harness is not a codebase that agents work on, but the environment, constraints, and feedback loops that enable agents to do reliable work.

## The Four Layers

### Layer 1: Agent Environment (Config-First)
Artifacts: SOUL.md, TOOLS.md, CLAUDE.md, AGENTS.md, openclaw.json, skills/

### Layer 2: Deterministic Feedback Loops (Agent-Orchestrator)
Deterministic reactions to predictable events: CI failed, changes requested, agent stuck

### Layer 3: LLM Judgment (OpenClaw)
Handles the 20% requiring judgment when deterministic reactions exhaust budget

### Layer 4: Entropy Management
Self-improving prompts, autonomous PR review, convergence intelligence

## Key Principles
1. Documentation as infrastructure
2. Deterministic first, LLM for judgment
3. Fresh context, not accumulated context
4. Build rippable harnesses
5. LLM decides, server executes

## Documentation-Driven Development (from OpenAI Workshop)

Ryan emphasizes codifying tribal knowledge into markdown files:

| File | Purpose |
|------|---------|
| reliability.md | Distributed systems principles (timeouts, retries) |
| security.md | Security guardrails and PII handling |
| architecture.md | High-level codebase topology (Matt Clad's approach) |
| agents.md | Persona/routing for triggering relevant docs |
| core_beliefs.md | Team culture, quality standards, user understanding |

## Philosophy Quote

> "The goal of Harness Engineering is to create an environment so deterministic and well-tested that the non-deterministic nature of LLMs is effectively corralled into producing consistently functional software."

## Evolution Path

1. **Greenfield** (new codebase) - Ideal for pushing autonomy boundaries
2. **Brownfield** (legacy codebase) - Accept 10x slower initially to build harnesses
3. **Nucleation points** - Create islands of efficiency that expand outward

## Related Concepts
- [[DualAgentArchitecture]] - Generator and Reviewer separation
- [[ProofOfWork]] - Mandatory PR evidence requirements
- [[MinimalReproLadder]] - TDD for AI agents
- [[ContextManagement]] - Attention vs. context exhaustion
