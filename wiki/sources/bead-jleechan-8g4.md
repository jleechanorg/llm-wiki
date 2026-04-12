---
title: "Regenerate disabled Slack xapp token"
type: source
tags: ["task", "p1", "bead"]
bead_id: "jleechan-8g4"
priority: P1
issue_type: task
status: open
created_at: 2026-02-19
updated_at: 2026-02-19
created_by: jleechan
source_repo: "."
---

## Summary
**[P1] [task]** Regenerate disabled Slack xapp token

## Details
- **Bead ID:** `jleechan-8g4`
- **Priority:** P1
- **Type:** task
- **Status:** open
- **Created:** 2026-02-19
- **Updated:** 2026-02-19
- **Author:** jleechan
- **Source Repo:** .

## Description

1. Go to https://api.slack.com/apps
2. Find "openclaw" app
3. Go to OAuth & Permissions
4. Regenerate xapp token (xapp-1-A0AESRKA7L3-... was disabled)
5. Update ~/.openclaw/openclaw.json with new token
6. Restart gateway: openclaw gateway restart

