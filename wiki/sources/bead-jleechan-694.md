---
title: "Launch readiness loop exits too early on lite-mode process exit causing false launch failures"
type: source
tags: ["bug", "p1", "bead"]
bead_id: "jleechan-694"
priority: P1
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P1] [bug]** Launch readiness loop exits too early on lite-mode process exit causing false launch failures

## Details
- **Bead ID:** `jleechan-694`
- **Priority:** P1
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

_wait_for_agent_launch_readiness breaks as soon as orchestrate subprocess exits, even in lite mode where process exits quickly and agent session may still be booting. This causes false `process_exited`/`no ready signal` failures while agent session exists or is about to exist.

