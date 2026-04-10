---
title: "Mission Auto-Completion"
type: concept
tags: [missions, automation, state-management, bug-fix]
sources: []
last_updated: 2026-04-08
---

Mission Auto-Completion is a system feature that automatically moves completed missions from active_missions to completed_missions when the LLM narrative indicates mission completion.

## Problem
Older campaigns (pre-fix) lack the completed_missions field, causing missions to remain stuck in active_missions even after narrative completion.

## Solution
Auto-initialization of completed_missions field when:
1. active_missions exists in campaign state
2. completed_missions is missing from campaign state
3. A state change is applied that affects missions

## Related
- [[ActiveMissionsField]] — source field for active missions
- [[CompletedMissionsField]] — destination field for completed missions
- [[CampaignStateMigration]] — transparent state migration
- [[Nocturne]] — production campaign affected by this bug
