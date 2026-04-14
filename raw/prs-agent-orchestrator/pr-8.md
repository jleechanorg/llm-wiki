# PR #8: feat(autonomy): close four lifecycle autonomy gaps

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-16
**Author:** jleechan2015
**Stats:** +2606/-110 in 17 files

## Summary
Closes four gaps identified in the 2026-03-15 code audit between AO's stated autonomy capabilities and the actual implementation.

## Test Plan
- [x] 489/492 tests pass (3 pre-existing `config.test.ts` env failures unrelated to this work)
- [x] New lifecycle-manager tests cover merge_conflicts event, request-merge action, context injection
- [ ] Manual: configure `auto-merge` reaction and verify `mergePR()` is called on merge-ready session

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> High risk because it changes core lifecycle/reaction behavior to optionally pe

## Raw Body
## Summary

Closes four gaps identified in the 2026-03-15 code audit between AO's stated autonomy capabilities and the actual implementation.

## Changes

### jleechan-514o · P1 · auto-merge stub
Wire `auto-merge` and new `request-merge` reactions to call `scm.mergePR()`:
- `auto-merge` now calls `mergePR()` directly after merge-ready state
- `request-merge` notifies human first, then calls `mergePR()` on approval
- `mergeMethod` config option (merge/squash/rebase, default: squash)

### jleechan-8p0s · P2 · merge-conflicts lifecycle event
Emit a real `merge-conflicts` event so reactions can fire on conflict:
- `merge_conflicts` added to `SessionStatus` and `SESSION_STATUS`
- Polling loop detects `!mergeReady.noConflicts` and emits event
- `agent-orchestrator.yaml.example` updated with example reaction

### jleechan-ylqd · P2 · context injection in repair prompts
`buildReactionContext()` appends structured context before dispatch:
- `ci-failed` → failing check names + status URLs via `scm.getCIChecks()`
- `changes-requested` → unresolved review thread summaries
- `merge-conflicts` → conflicting file list hints

### jleechan-4xzz · P3 · hook observer documentation
Clarify agent plugin hooks are PostToolUse observers, not interceptors:
- `agent-claude-code` and `agent-codex` comments rewritten
- `TODO(interception)` stubs left for future pre-command needs

## Test plan

- [x] 489/492 tests pass (3 pre-existing `config.test.ts` env failures unrelated to this work)
- [x] New lifecycle-manager tests cover merge_conflicts event, request-merge action, context injection
- [ ] Manual: configure `auto-merge` reaction and verify `mergePR()` is called on merge-ready session

🤖 Generated with [Claude Code](https://claude.com/claude-code)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **High Risk**
> High risk because it changes core lifecycle/reaction behavior to optionally perform SCM merges and adds new session states/events, plus a large rewrite of the `agent-claude-code` plugin im
