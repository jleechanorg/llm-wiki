---
title: "merge-conflicts missing lifecycle event: no send-to-agent reaction possible"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-8p0s"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** merge-conflicts missing lifecycle event: no send-to-agent reaction possible

## Details
- **Bead ID:** `jleechan-8p0s`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

getMergeability() in scm-github/src/index.ts returns merge conflicts as blockers, but lifecycle-manager never emits a merge-conflicts lifecycle event. Without this event, no reaction (send-to-agent, notify) can be configured to fire when a PR has conflicts. Add a merge-conflicts event emission and reaction path.

