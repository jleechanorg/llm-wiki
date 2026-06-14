---
title: "System Instruction Prefix Stability Audit (Real HTTP Capture)"
type: source
tags: ["system-instruction", "prefix-stability", "cache-redesign", "worldarchitect-ai", "bead-rev-n6nbs"]
date: 2026-06-04
source_file: project_2026-06-04_system_instruction_prefix_stability_audit.md
---

## Summary
Empirical wire-level capture: only master_directive (~18.6K chars/~4.6K tok) is truly-static cross-agent prefix. The ~37K-tok game_state block is static TEXT but position-shifted by dynamic identity block inserted at agent_prompts.py:2650. Reorder unlocks shared per-agent cache.

## Key Claims
- Truly-static cross-agent prefix = master_directive.md only: chars 0..18,639 (~4.6K tok), byte-identical across ALL 17 requests
- NO dynamic IDs injected into system_instruction: zero campaign_id, zero UUIDs (42 '20-char id' regex hits were false positives — CamelCase schema words)
- NO injected real-world dates/timestamps: every date/time token is STATIC (doc-version headers, JSON schema EXAMPLE values)
- Within a stable window the WHOLE system_instruction is byte-identical (records 22-32 = 6 consecutive same-agent requests identical end-to-end)
- ROOT CAUSE: `agent_prompts.py:2650` `parts.insert(1, identity_block)` inserts dynamic Character Identity block at index 1 — between master_directive and ~37K-tok static game_state_instruction.md
- Viable design: SINGLE shared explicit cache holding ONLY globally-identical system_instruction+tools, OR implicit-only (75% discount, ZERO storage, ~1,024-tok min prefix)

## Key Quotes
> Hard safety boundary: a shared cache may contain ONLY globally-identical system+tools — NEVER user_id, campaign prompts, world/character data, story, or memories

## Connections
- [[SystemInstruction]] — concept
- [[GeminiCache]] — design A
- [[CacheRedesign]] — broader concept
