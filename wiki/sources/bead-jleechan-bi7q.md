---
title: "ComponentValidationTestBase.validate_component() never called in schema tests — tracking is dead code"
type: source
tags: ["chore", "p3", "bead"]
bead_id: "jleechan-bi7q"
priority: P3
issue_type: chore
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P3] [chore]** ComponentValidationTestBase.validate_component() never called in schema tests — tracking is dead code

## Details
- **Bead ID:** `jleechan-bi7q`
- **Priority:** P3
- **Type:** chore
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

All schema tests that inherit from `ComponentValidationTestBase` report `total_validations: 0` in `component_validation_summary.json`. The `validate_component()` method on the base class is never called by `run_scenarios()` in any of:

- `test_schema_validation_fallback.py`
- `test_schema_validation_extended.py`
- `test_schema_migration_flow_real_api.py`
- `test_schema_validation_real_api.py`

Each test uses its own custom validation functions (`validate_schema_structure`, `validate_firestore_persistence`, etc.) instead of the base class component tracking. The `component_validation_summary.json` artifact is generated but contains no useful data for these tests.

The `schema_enforcement_journey` test uses a different summary (`schema_validation_summary.json`) which DOES have real data (10 validations).

File: `testing_mcp/lib/component_validation_test_base.py`

