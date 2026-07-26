---
title: "Manual cmux restore requires explicit approval"
type: source
tags: [cmux, authorization, restore, policy]
sources:
  - raw/feedback_2026-07-12_manual_cmux_restore_requires_approval.md
last_updated: 2026-07-12
---

## Summary
This source records a hard authorization rule for manual cmux restoration. Manual restore actions are forbidden unless the most recent live user message both requests the restore and includes the exact case-sensitive phrase `CMUX RESTORE APPROVED`. The note also distinguishes manual restore from safe read-only diagnostics, backup creation, and cmux's normal automatic app-start restoration.

## Key Claims
- Manual cmux restore is disallowed unless the latest live user message explicitly requests it and contains `CMUX RESTORE APPROVED`.
- Earlier restore instructions, summaries, goals, or policy discussion do not authorize a later manual restore.
- A newer stop or read-only instruction revokes any earlier restore intent.
- The gate covers `cmux restore-session`, `session.restore_previous`, active session-file replacement for restoration, and manual reconstruction or resume of saved coding-agent surfaces.
- Read-only diagnostics, backup creation, and automatic restoration when the user opens cmux remain allowed.

## Key Quotes
> "Do not manually restore cmux workspaces, surfaces, active session files, or saved coding-agent processes"

> "A newer stop or read-only instruction always revokes earlier restore intent."

## Connections
- [[ManualCmuxRestoreApprovalGate]] — the concrete authorization rule extracted from this source
- [[CommitmentIntegrity]] — do not continue a restore path after the user has said stop
