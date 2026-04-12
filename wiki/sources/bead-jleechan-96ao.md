---
title: "Schema migration triggered by GOD_MODE __DELETE__, not by normal character action as designed"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-96ao"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Schema migration triggered by GOD_MODE __DELETE__, not by normal character action as designed

## Details
- **Bead ID:** `jleechan-96ao`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

In `test_schema_migration_flow_real_api`, the "one-time schema migration" is supposed to be triggered by the first normal character action after a legacy-state setup. However, the MCP request trace shows:

- Entry [6] (god mode `apply_god_mode_update_and_fetch` with `__DELETE__` keys) triggers migration: warning `"Applied one-time schema migration for legacy compatibility"` with new `migrated_at` timestamp (21:22:35)
- Entry [9] (character mode process_action "I look around carefully.") shows NO migration warning — migration was already done

Additionally, two distinct `migrated_at` timestamps exist (21:22:33 from ensure_story_mode setup, 21:22:35 from the legacy_update call), meaning the "one-time" migration ran at least twice.

The test passes because it only validates the final state (migration_version=1, valid timestamp) without asserting WHICH action triggered the migration or that it ran exactly once.

Evidence: `/tmp/worldarchitectai/schema_followup/schema_migration_flow_real_api/latest/request_responses.jsonl` entries [6] vs [9]

File: `testing_mcp/schema/test_schema_migration_flow_real_api.py`

