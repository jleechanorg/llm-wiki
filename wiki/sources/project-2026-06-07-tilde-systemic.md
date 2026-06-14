---
title: "Tilde expansion is systemic, not a one-off bug"
type: source
tags: [tilde, systemic, expandHome, centralization, agent-orchestrator]
date: 2026-06-07
source_file: raw/project_2026-06-07_tilde_systemic.md
---

## Summary
The antigravity tilde bug in PR #654 (commit 97b51e6ff) is a symptom, not the disease. 14 tilde-related defects across 8 files. Canonical expandHome helper in packages/core/src/paths.ts:186-191 is exported and used by lifecycle-worker.ts, spawn.ts, config.ts:466,1013, env-source.ts:104 — but plugin authors and CLI author rolled their own. Two anti-patterns: (1) path.replace(/^~/, process.env['HOME'] || '') — 7 instances in packages/cli/src/commands/start.ts; (2) per-plugin local expandPath(p) functions — 5 near-copies.

## Key Claims
- 14 tilde-related defects across 8 files; canonical expandHome exists in core/paths.ts:186 but not used by 5 per-plugin copies and 7 inline regexes in start.ts
- Anti-pattern 1: path.replace(/^~/, process.env['HOME'] || '') — 7 instances in start.ts:361,524,743,986,1029,1121,1221 — only strips ^~ (1 char), not ^~/ (2 chars), so ~/foo becomes /home/foo correctly but ~weird becomes /homeweird incorrectly
- Anti-pattern 2: per-plugin local expandPath(p) functions — 5 near-copies in workspace-worktree, workspace-clone, scm-github, backfill-extensions, recovery/workspacePolicy
- Shipped fix in packages/plugins/agent-antigravity/src/index.ts:304-315 handles ~/ and bare ~ correctly with path.join(userHome, p.slice(2)) and 6-assertion TDD test at index.test.ts:647-690
- Follow-up: extend expandHome to handle bare ~ (currently latent bug), replace 5 plugin copies, replace 7 inline regexes, add test matrix (~, ~/, /abs/path, relative/path, empty, HOME unset, ~user/)

## Connections
- [[feedback_2026-04-04_tilde_slice_bug]]
- [[ExpandHome]]
- [[TildeSystemic]]
