---
title: "Completed Missions Auto-Initialization Tests"
type: source
tags: [python, testing, migration, backward-compatibility, firestore]
source_file: "raw/test_completed_missions_auto_init.py"
sources: []
last_updated: 2026-04-08
---

## Summary
Test suite validating the fix for a backward compatibility bug where older campaigns lack the completed_missions field, preventing mission auto-completion. The tests verify that completed_missions is auto-initialized when active_missions exists but completed_missions does not.

## Key Claims
- **Bug Location**: Production Nocturne campaign had active_missions but no completed_missions field
- **Problem**: Missions couldn't auto-complete because there was nowhere to move completed missions
- **Solution**: Auto-initialize completed_missions as empty list when active_missions exists but completed_missions doesn't
- **Preservation**: Existing completed_missions data must not be overwritten

## Key Test Cases
- test_auto_init_when_active_missions_exists_but_completed_doesnt — RED test validating auto-creation
- test_auto_init_when_state_has_active_missions_at_start — validates init at function start
- test_no_auto_init_when_completed_missions_already_exists — ensures no data loss
- test_no_auto_init_when_no_active_missions_field — only creates when needed
- test_completed_missions_smart_conversion — supports dict→list conversion

## Connections
- [[FirestoreService]] — where update_state_with_changes is implemented
- [[StateMigration]] — concept for backward-compatible schema evolution

## Contradictions
- None identified
