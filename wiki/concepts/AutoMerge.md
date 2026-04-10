---
title: "Auto-Merge"
type: concept
tags: [auto-merge, automation, github-actions]
sources: []
last_updated: 2026-04-07
---

## Definition
Auto-merge is a GitHub feature that automatically merges a PR when all required checks pass. In the AO/Cursor workflow, this is controlled by skeptic-cron workflow but can be disabled via configuration.

## Controls
- **Enable all**: Set `SKEPTIC_CRON_AUTO_MERGE` to `true` or delete variable
- **Disable all**: Set `SKEPTIC_CRON_AUTO_MERGE` to `false`
- **Selective hold**: Add PR numbers to `SKEPTIC_MERGE_DENYLIST`

## Use Case
Auto-merge is disabled for PRs requiring manual verification or when coordination with other PRs is needed before merging.
