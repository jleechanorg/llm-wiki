---
title: "pairv2: increase max_cycles and retry on NEEDS_HUMAN before escalating to human review"
type: source
tags: ["feature", "p1", "bead"]
bead_id: "jleechan-vo1m"
priority: P1
issue_type: feature
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [feature]** pairv2: increase max_cycles and retry on NEEDS_HUMAN before escalating to human review

## Details
- **Bead ID:** `jleechan-vo1m`
- **Priority:** P1
- **Type:** feature
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

pairv2 currently exits with NEEDS_HUMAN verdict after max_cycles (default 3) without retrying fixable gaps. Instead it should: (1) on NEEDS_HUMAN, feed verifier feedback back to coder as a new cycle, (2) only escalate to human after N consecutive NEEDS_HUMAN cycles with no delta progress, (3) raise default max_cycles from 3 to at least 5. Current behavior wastes the coder's ability to self-correct on issues like missing files or misnamed modules.

