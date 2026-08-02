---
title: "Read-only repository scope preserves explicit close-out actions"
type: source
tags: [scope, operational-boundaries, permissions, readonly, persistence]
date: 2026-07-29
source_file: /Users/jleechan/.claude/projects/-Users-jleechan-projects-worktree_ci_trim/memory/feedback_2026-07-29_readonly_scope_preserves_explicit_closeout.md
bead: rev-ip5un
---

## Summary

`read-only` scopes to repository surfaces (code, workflows, tests, docs) and does NOT erase independently authorized operational actions like `/up`, `/learn`, bead creation, or goal setting in the same message. Explicit broader phrases like `no changes` override this default.

## Key Claims

- `readonly` forbids repository edits but preserves separately requested beads, goals, `/learn`, and `/up` persistence
- Independent authorizations in the same live user message are NOT cancelled by `readonly` scope
- Explicit authorizations (e.g., "close bead X", `/learn <topic>`) continue to execute
- Broader phrases (`no changes`, `no mutations`) override this scoped default

## Key Quotes

> "Treat `read-only` as scoped to the repository surfaces named by the task. It does not erase independent authorizations in the same live message."

> "Continue explicitly requested beads, goals, `/learn`, `/up`, metadata, and review artifacts, but do not infer permission for pushes, PR comments or state changes, merges, deployments, or unrelated external messages."

## Connections

- [[Readonly Scope Skill]] — canonical skill definition
- [[Permissions and Authorization]] — scope boundaries
- [[Beads Issue Tracking]] — persistent artifact creation during readonly
- [[Harness Guardrails]] — enforcement layer
- Bead `rev-ip5un` — issue tracking for this rule clarification

## Implementation

**FIX:** Canonicalized rule in `~/.claude/skills/readonly-scope/SKILL.md` on 2026-07-29. One full definition + five pointers across Claude, Codex, Gemini, Cursor, and Hermes always-loaded surfaces.

**References:**
- `~/.claude/skills/readonly-scope/SKILL.md` (canonical)
- `~/.claude/commands/up.md` (single-writer rule)
- Operator clarification 2026-07-29

