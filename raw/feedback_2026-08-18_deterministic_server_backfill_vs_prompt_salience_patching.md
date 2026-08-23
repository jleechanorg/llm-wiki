---
name: deterministic server backfill vs prompt salience patching
description: When BigQuery forensic data shows models drop structured JSON fields during long outputs despite 100% prompt reminder presence, prefer deterministic server-side extraction and backfill from verified execution stdout over prompt-level salience stacking.
type: feedback
bead: rev-ijl9c
---

# Deterministic Server Backfill vs Prompt Salience Patching

## Context
During PR #9025 (commit `5d384f8531`), the team investigated why `gemini-3.7-flash` intermittently dropped `action_resolution.mechanics.rolls` from its JSON output on code_execution turns. The initial instinct was to add a tail/recency-anchor reminder (`DICE EXECUTION ENFORCEMENT`) across all agents.

## Technical Detail & Empirical Evidence
1. **BigQuery Forensics (`worldarchitecture-ai.llm_forensics.llm_payloads`)**:
   - Querying production turns where `gemini-3.7-flash` executed Python code revealed a **33.3% to 44.4% native emission rate** of the rolls JSON across `StoryModeAgent` and `CombatAgent`.
   - `FactionManagementAgent` already had the prompt reminder on the wire in **100% of turns (n=142)**, yet had the highest loss rate (~90%) in the fleet.
   - Attention drop occurs during long structured JSON generation (multi-page prose + planning block), causing the model to skip copying Python stdout numbers into JSON regardless of prompt salience.
2. **Deterministic Server Backfill (`mvp_site/dice_integrity.py`)**:
   - The backend owns verified Python execution stdout from the code-execution tool.
   - `apply_dice_audit_resolution()` intercepts responses: if `action_resolution.mechanics.rolls` is empty, it parses RNG-verified stdout, applies strict fabrication guards (identity matching against fresh stdout), and backfills the array.
   - This provides a 100% mathematical guarantee with zero reliance on model copy compliance.

## Rule & Reusable Pattern
- **Do not infinitely stack recency-anchor prompt reminders** when a model exhibits attention drop on structured field copying.
- **Strip dead prompt reminders** to save prompt tokens and reduce agent boilerplate.
- **Rely on deterministic server-side backfill** whenever the backend already owns verified tool/code execution outputs.
- **Enforce fabrication guards**: Any server backfill must verify authenticity and match identity before populating user-visible schema fields.

## References
- PR: https://github.com/jleechanorg/worldarchitect.ai/pull/9025
- Commit: `5d384f8531`
- Bead: `rev-ijl9c`
- BigQuery Table: `worldarchitecture-ai.llm_forensics.llm_payloads`
- Core Implementation: `mvp_site/dice_integrity.py:apply_dice_audit_resolution`
