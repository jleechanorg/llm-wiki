---
title: "WorldArchitect.AI System Architecture v3.0"
type: source
tags: [architecture, game-engine, dnd, gemini, fastembed, token-budget, dice-integrity, faction]
date: 2026-05-16
source_file: docs/design/system-architecture.md
---

## Summary
Deep architecture doc for WorldArchitect.AI — covers the 14-agent semantic routing system, prompt engineering library (30 files, 17K lines), deterministic 5-component token budget engine, dice anti-fabrication protocol, living world faction system, and deployment topology. All line counts verified against source code.

## Key Claims
- 14 specialized agents route via FastEmbed cosine similarity (no keyword matching)
- 30 prompt files with `<!-- ESSENTIALS -->` compression reduce tokens by up to 80%
- Token budget: min-first/fill-to-max, story context guaranteed ≥30%
- Dice anti-fabrication: LLM requests rolls, Gemini code-execution sandbox resolves them
- 12 living world factions with autonomous background ticks
- LLM-Decides/Server-Executes pattern: server validates all LLM state proposals
- Three-stage context compression: comment strip → essentials → field drop
- All line counts independently verified against source (world_logic 9,930; llm_service 9,072; game_state 4,424; agents 3,844; agent_prompts 2,846)

## Key Quotes
> "LLM Decides, Server Executes — the LLM proposes operations, the server validates and persists them" — Core architecture principle
> "Every prompt file contains an `<!-- ESSENTIALS -->` block — a condensed version of critical rules" — Essentials mode design
> "Keywords are fragile — 'I want to fight' and 'let's do battle' route differently with keywords, identically with embeddings" — Why FastEmbed

## Connections
- [[WorldArchitectAI]] — the platform this documents
- [[FastEmbed]] — embedding model for semantic routing
- [[DiceIntegrity]] — anti-fabrication protocol
- [[TokenBudget]] — deterministic budget allocation
- [[FactionSystem]] — living world factions
- [[GeminiAPI]] — primary LLM backend
