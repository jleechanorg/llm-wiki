---
title: "restart-on-reboot.sh swallows monitor.sh errors"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-p7xy"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** restart-on-reboot.sh swallows monitor.sh errors

## Details
- **Bead ID:** `jleechan-p7xy`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The `./monitor.sh || true` on line 35 swallows all errors including permission denied, script not found. If monitor.sh fails silently, the loop continues with potentially broken state. Should capture and log actual exit code.

