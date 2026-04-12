---
title: "Local UI sometimes sends malformed Bearer token (`fake-token`) causing repeated 401 traceback noise"
type: source
tags: ["bug", "p2", "bead"]
bead_id: "jleechan-06o"
priority: P2
issue_type: bug
status: open
created_at: 2026-02-20
updated_at: 2026-02-20
created_by: jleechan2015
source_repo: "."
---

## Summary
**[P2] [bug]** Local UI sometimes sends malformed Bearer token (`fake-token`) causing repeated 401 traceback noise

## Details
- **Bead ID:** `jleechan-06o`
- **Priority:** P2
- **Type:** bug
- **Status:** open
- **Created:** 2026-02-20
- **Updated:** 2026-02-20
- **Author:** jleechan2015
- **Source Repo:** .

## Description

During local server runs, protected endpoints intermittently receive `Authorization: Bearer fake-token`, which triggers Firebase token decode exceptions (`Wrong number of segments`) and repeated 401s in logs.

Evidence:
- `/tmp/worktree_clawi/revert-5581-revert-5580-codex_implement-openclaw-gateway-communication-vf7ma8/flask_backend.log`
- timestamps: `2026-02-19 17:07:38`, `17:15:45`, `18:17:48`
- endpoints affected around latest occurrence: `GET /api/campaigns`, `POST /api/campaigns`.

Current behavior impact:
- Functional flow continues for authenticated session, and OpenClaw routing works after settings save.
- But logs are polluted with stack traces and auth failures from malformed token traffic, obscuring real failures and making local diagnostics brittle.

