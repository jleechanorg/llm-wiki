---
title: "Heartbeat cron missing exit code validation"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-dp0n"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Heartbeat cron missing exit code validation

## Details
- **Bead ID:** `jleechan-dp0n`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The heartbeat cron job at setup line 273 runs `./run.sh --once` but never validates the exit code. Failed runner starts won't be detected until next monitor check (15 min later). Should capture exit code and log failures.

