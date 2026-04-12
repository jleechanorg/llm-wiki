---
title: "Phase 1: Remove orphaned LaunchAgents (consensus, symphony, disabled PR-automation)"
type: source
tags: ["task", "p2", "bead"]
bead_id: "jleechan-jtm8"
priority: P2
issue_type: task
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [task]** Phase 1: Remove orphaned LaunchAgents (consensus, symphony, disabled PR-automation)

## Details
- **Bead ID:** `jleechan-jtm8`
- **Priority:** P2
- **Type:** task
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

Remove ai.openclaw.consensus.plist (stale 2nd gateway port 18790, v2026.2.12), ai.symphony.daemon.plist (exits 127, broken), ai.worldarchitect.pr-automation.fixpr.plist.disabled, ai.worldarchitect.pr-automation.fix-comment.plist.disabled. Quick wins, no risk. See roadmap/SIMPLIFICATION_PLAN.md.

