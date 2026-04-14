---
title: "Schema Validation As Warning"
type: concept
tags: [pairv2, bug-pattern, automation]
sources: []
last_updated: 2026-04-13
---

## Description

The schema validation as warning pattern treats schema validation failures as warnings rather than hard-fail verdicts. Schema validation failures (field name typos, version mismatches, missing optional fields) do not mean the code is wrong — the verifier should evaluate the actual code.

## Why It Matters

`_verify_right_contract_node` was returning immediate `verdict=FAIL` when schema validation fails. This overrides the verifier's ability to evaluate whether the actual implementation is correct. Schema validation is a syntactic check, not a semantic one.

## Key Technical Details

- **Pattern**: Schema validation failures should be warnings, not hard-fail verdicts
- **Scope**: `.claude/pair/pair_execute_v2.py` — `_verify_right_contract_node()`
- **Key insight**: Let the verifier evaluate the code, not just the schema

## Related Beads

- BD-pairv2-schema-hard-fail
