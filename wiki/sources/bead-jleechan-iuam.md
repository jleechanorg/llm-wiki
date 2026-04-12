---
title: ".openclaw_prod is intentionally NOT a git repo (prod deployment dir)"
type: source
tags: ["reference", "p2", "bead"]
bead_id: "jleechan-iuam"
priority: P2
issue_type: reference
status: open
created_at: 2026-04-04
updated_at: 2026-04-04
created_by: jleechan
source_repo: "."
---

## Summary
**[P2] [reference]** .openclaw_prod is intentionally NOT a git repo (prod deployment dir)

## Details
- **Bead ID:** `jleechan-iuam`
- **Priority:** P2
- **Type:** reference
- **Status:** open
- **Created:** 2026-04-04
- **Updated:** 2026-04-04
- **Author:** jleechan
- **Source Repo:** .

## Description

~/.openclaw_prod is the production runtime directory created by PR #485 (merged 2026-04-04). It is NOT a git repo by design.

Layout:
- ~/.openclaw = staging git repo (port 18810, branch dev1775263735)
- ~/.openclaw_prod = production deployment dir (port 18789), created via deploy pipeline from staging

~/.openclaw_prod contains:
- Symlinks to ~/.openclaw: agents, credentials, extensions, HEARTBEAT.md, lcm.db, SOUL.md, TOOLS.md
- Own runtime state: cron, delivery-queue, devices, identity, memory, openclaw.json, canvas, logs, update-check.json

The 'git status' fatal error in ~/.openclaw_prod is expected and correct. Source of truth is ~/.openclaw (jleechanorg/jleechanclaw repo).

