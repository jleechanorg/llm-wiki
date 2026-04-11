---
title: "PR #196: docs: add Value Router design proposal"
type: source
tags: []
date: 2026-03-16
source_file: raw/prs-worldai_claw/pr-196.md
sources: []
last_updated: 2026-03-16
---

## Summary
- **MergeValue formula**: (P_merge_24h * BusinessImpact * StrategicFit * Confidence) / ExpectedAgentHours
- Turns AO from "automation runner" into a self-optimizing execution system
- Compounds throughput and merge quality without increasing operator overhead

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Mostly documentation changes plus small `ao-backfill.sh` jq/logging adjustments; low risk aside from potentially altering which PRs get picked up by the backfill cron.
> 
> **Overview

## Metadata
- **PR**: #196
- **Merged**: 2026-03-16
- **Author**: jleechan2015
- **Stats**: +83/-6 in 5 files
- **Labels**: none

## Connections
