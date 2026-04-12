---
title: "agent wrapper hooks are PostToolUse not true interception"
type: source
tags: ["bug", "p3", "bead"]
bead_id: "jleechan-4xzz"
priority: P3
issue_type: bug
status: open
created_at: 2026-03-15
updated_at: 2026-03-15
created_by: jleechan
source_repo: "."
---

## Summary
**[P3] [bug]** agent wrapper hooks are PostToolUse not true interception

## Details
- **Bead ID:** `jleechan-4xzz`
- **Priority:** P3
- **Type:** bug
- **Status:** open
- **Created:** 2026-03-15
- **Updated:** 2026-03-15
- **Author:** jleechan
- **Source Repo:** .

## Description

The Claude Code and Codex agent plugins install PostToolUse bash hooks that fire AFTER gh pr create / gh pr merge complete. This updates AO metadata correctly but cannot intercept or modify command behavior. Documentation and marketing copy overstate this as interception. Consider whether true pre-command interception is needed, or just correct the documentation.

