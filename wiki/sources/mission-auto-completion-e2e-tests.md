---
title: "Mission Auto-Completion E2E Tests"
type: source
tags: [python, testing, e2e, missions, state-migration]
source_file: "raw/test_mission_auto_completion_e2e.py"
sources: []
last_updated: 2026-04-08
---

## Summary
End-to-end test for mission auto-completion with completed_missions auto-initialization. Tests the fix for the bug where older campaigns don't have the completed_missions field, preventing missions from auto-completing.

## Key Claims
- **Auto-initialization**: completed_missions field is automatically initialized when active_missions exists but completed_missions is missing
- **Mission completion logic**: Completed missions move from active_missions to completed_missions automatically
- **Older campaign migration**: Legacy campaign states are migrated transparently without manual intervention
- **Smart conversion**: Supports dict-to-list format conversion for completed_missions

## Key Quotes
> "Production Nocturne campaign had active_missions but no completed_missions field"
> "Missions stayed in active_missions even after narrative completion"
> "Required manual god mode intervention to close"

## Connections
- [[ActiveMissionsField]] — source of missions before completion
- [[CompletedMissionsField]] — destination for completed missions
- [[Nocturne]] — production campaign affected by this bug
- [[CampaignStateMigration]] — transparent migration of legacy campaign states

## Contradictions
- None identified
