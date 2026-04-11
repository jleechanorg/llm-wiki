---
title: "Social HP Server Enforcement Markers Removed"
type: source
tags: [tdd, unit-testing, social-hp, refactoring, python]
source_file: "raw/social-hp-server-enforcement-markers-removed.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Unit test validating that SOCIAL_HP enforcement markers have been removed from llm_service.py. Verifies the removal of injection, scaling, progress sync, and resistance tracking markers as part of the social HP cleanup effort.

## Key Claims
- **Marker Removal**: All SOCIAL_HP_* enforcement markers must be removed from llm_service.py
- **Markers Verified**: INJECT, SCALE, PROGRESS_SYNC, and RESISTANCE markers are no longer present
- **Code Clean**: The removal indicates social HP mechanics have been decoupled from server-side enforcement

## Key Test Function
- `test_social_hp_server_enforcement_markers_removed`: Verifies each marker string is not present in llm_service.py

## Connections
- [[social-hp-enforcement-reminder-tests]] — related to social HP enforcement testing
- [[social-hp-challenge-schema-derived-enums-tests]] — related to social HP schema validation

## Contradictions
- None identified
