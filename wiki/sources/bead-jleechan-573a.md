---
title: "agent-base duplicates agent-claude-code logic without consolidating original"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-573a"
priority: P2
issue_type: bug
status: open
created_at: 2026-03-17
updated_at: 2026-03-17
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [bug]** agent-base duplicates agent-claude-code logic without consolidating original

## Details
- **Bead ID:** `jleechan-573a`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-17
- **Updated:** 2026-03-17
- **Author:** jleechan
- **Source Repo:** .

## Description

agent-base is a near-complete copy of agent-claude-code internal logic (launch/env/session/process detection). agent-claude-code was not refactored to use agent-base — it just wraps createAgentPlugin(). Same logic lives in two places. agent-claude-code should fully delegate to agent-base to eliminate duplication.

