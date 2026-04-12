---
title: "@reboot cron uses install-time RUNNER_DIR"
type: source
tags: ["bug", "p3", "bead"]
bead_id: "jleechan-0lp0"
priority: P3
issue_type: bug
status: open
created_at: 2026-02-21
updated_at: 2026-02-21
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P3] [bug]** @reboot cron uses install-time RUNNER_DIR

## Details
- **Bead ID:** `jleechan-0lp0`
- **Priority:** P3
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-21
- **Updated:** 2026-02-21
- **Author:** jleechan2015
- **Source Repo:** .

## Description

The @reboot cron at setup line 270 uses hardcoded path `${RUNNER_DIR}` which is set at install time. If RUNNER_DIR changes or the script is moved, the cron will fail silently. Consider using full paths or validating at cron runtime.

