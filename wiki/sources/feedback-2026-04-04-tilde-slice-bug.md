---
title: "Tilde path expansion — use slice(2) not slice(1)"
type: source
tags: [tilde, slice-bug, path-expansion, node-js, agent-orchestrator]
date: 2026-04-04
source_file: raw/feedback_2026-04-04_tilde_slice_bug.md
---

## Summary
When expanding ~ in config paths, use slice(2) not slice(1) to skip the ~/ two-character prefix. slice(1) only skips the ~ and leaves a leading / ("~/.foo".slice(1) = "/.foo" treated as absolute). Correct approach: path.join(os.homedir(), dir.slice(2)) or os.homedir() + dir.slice(1) — both handle ~/ prefix correctly. Recurrence: same bug class re-surfaced 64 days later in packages/plugins/agent-antigravity/src/index.ts (PR #654, commit 97b51e6ff) — fix at line 305 correctly uses slice(2).

## Key Claims
- slice(1) only skips ~ and leaves leading / ("~/.foo".slice(1) = "/.foo" treated as absolute path by Node.js)
- slice(2) skips ~/ and leaves ".foo" (relative) — correct approach
- Canonical: dir.startsWith("~/") ? join(os.homedir(), dir.slice(2)) : dir
- Same class of bug re-surfaced 64 days later in packages/plugins/agent-antigravity/src/index.ts (PR #654, commit 97b51e6ff)

## Connections
- [[project_2026-06-07_tilde_systemic]]
- [[TildePathExpansion]]
- [[TildeSliceBug]]
