# PR #5: feat(claim-pr): send initial task message to agent after claiming PR

**Repo:** jleechanorg/agent-orchestrator
**Merged:** 2026-03-16
**Author:** jleechan2015
**Stats:** +304/-10 in 7 files

## Summary
- Agents spawned with `--claim-pr` had no initial instructions — they woke up in the worktree not knowing they should fix a PR
- This caused agents to idle, exit early, or post `@coderabbitai all good?` without reading/fixing review comments
- Root cause: `claimPR()` checked out the branch and updated metadata but sent zero message to the agent

## Raw Body
## Summary
- Agents spawned with `--claim-pr` had no initial instructions — they woke up in the worktree not knowing they should fix a PR
- This caused agents to idle, exit early, or post `@coderabbitai all good?` without reading/fixing review comments
- Root cause: `claimPR()` checked out the branch and updated metadata but sent zero message to the agent

## Changes
- **`types.ts`**: Add `sendInitialMessage?: boolean` to `ClaimPROptions`
- **`session-manager.ts`**: `claimPR()` calls `send()` with a structured task message when `sendInitialMessage: true`; exports `buildInitialPRTaskMessage()` helper
- **`spawn.ts`** (CLI): `spawn --claim-pr` passes `sendInitialMessage: true` by default
- **`session-manager.test.ts`**: 3 TDD tests (sends when true, no-op when omitted, no-op when false)

## Initial message tells the agent to
1. Read all PR comments (`gh pr view N --comments`)
2. Read bot reviews (`gh api .../reviews`)
3. Read inline comments (`gh api .../comments`)
4. Check CI (`gh pr checks`)
5. Fix every actionable item, push
6. Only after all comments resolved: post `@coderabbitai all good?`
7. If merge conflicts: rebase on default branch first

## Testing
- 3 new TDD unit tests, all green
- Full core test suite: 479/479 passing (2 pre-existing config.test failures are env-specific, exist on main before this change)

<!-- CURSOR_SUMMARY -->
---

> [!NOTE]
> **Low Risk**
> Low risk: adds an optional post-claim message dispatch and tests, with failures explicitly treated as non-fatal and no changes to auth/data handling.
> 
> **Overview**
> Adds an opt-in `ClaimPROptions.sendInitialMessage` flag so `claimPR()` can immediately `send()` a structured PR-fix task message (built by new `buildInitialPRTaskMessage()`) after checkout/assignment.
> 
> Updates `ao spawn --claim-pr` to enable this by default, and adds unit tests covering message generation (including `owner/repo` in `gh` commands) plus send-on/skip behavior. Also starts tracking new repo-level agent guideline f
