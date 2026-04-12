---
title: "Invalid `in_combat: \"nope\"` persists to Firestore despite schema warning"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-2tbb"
priority: P1
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [bug]** Invalid `in_combat: "nope"` persists to Firestore despite schema warning

## Details
- **Bead ID:** `jleechan-2tbb`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

In `test_schema_validation_fallback` scenario 2, `combat_state.in_combat` is set to the string `"nope"` (invalid boolean). The server issues a schema warning but the invalid value persists in Firestore. Confirmed in evidence: entries [29] and [30] of `request_responses.jsonl` both show `in_combat: nope` after the update.

Root cause: The "warnings not asserts" philosophy means schema violations are logged but not rejected. Invalid typed data reaches Firestore.

Evidence: `/tmp/worldarchitectai/schema_followup/schema_validation_fallback/latest/request_responses.jsonl` entries [29-30]

Test file: `testing_mcp/schema/test_schema_validation_fallback.py` line 173-177

