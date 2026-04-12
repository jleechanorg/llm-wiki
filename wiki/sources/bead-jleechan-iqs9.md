---
title: "Schema extended test failure: consumable scenario missing expected updates"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-iqs9"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Schema extended test failure: consumable scenario missing expected updates

## Details
- **Bead ID:** `jleechan-iqs9`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The `testing_mcp/schema/test_schema_validation_extended.py` suite still fails the `Use consumable item (healing potion)` scenario after recent validator fixes. In `/tmp/worldarchitectai/schema_followup/schema_validation_extended/iteration_005/run.json`, scenario fails with `resources is missing but expected in expected_updates` and `inventory/backpack is missing but expected in expected_updates`.

Root state seen in evidence indicates state persisted as full `player_character_data` with `inventory`/`equipment.backpack` but no direct `resources`/inventory delta in `state_updates` for this action, causing strict expected-update checks to fail. Need to unblock by either:
- updating validation expectations to match actual action output shape for consumable scenario in this suite, or
- updating action output generation to include explicit resource and inventory delta fields in state_updates for consumable use.

