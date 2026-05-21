# Evidence Test Design — WorldArchitect.AI testing_mcp

## Core Rule: process_action for LLM behavior, not get_campaign_state

When verifying LLM-driven `planning_block` content in `testing_mcp/` evidence tests:

- **Use `ctx.process_action(campaign_id, user_input, mode=...)`** — triggers a fresh LLM inference pass in the current game state
- **Never use `ctx.get_campaign_state(campaign_id)`** for planning_block verification — returns cached story-start planning_block that may have stale speculative choices

## Why get_campaign_state is Unsafe for planning_block Assertions

`get_campaign_state_unified` → `_reconcile_level_up_ui_pair` preserves cached level-up choices when both:
- `rewards_box.level_up_available == True`
- `planning_block` already has level-up choices

This means cached speculative mechanic choices survive even after seeding entry state, causing false failures.

## Campaign Description Discipline

Use **neutral** campaign descriptions that do not hint at the mechanic being tested:
- ❌ `"A combat arena for testing level-up entry behavior"` — causes LLM to speculatively return level-up mechanic choices at story start
- ✅ `"A stone fortress where adventurers hone their skills"` — neutral, LLM follows protocol cues instead

## Source

- PR [#6958](https://github.com/jleechanorg/worldarchitect.ai/pull/6958) — evidence iteration 3 (2026-05-19)
- Memory: project_2026-05-19_pr6958_evidence_iteration3.md
- Bead: rev-ee0u8
