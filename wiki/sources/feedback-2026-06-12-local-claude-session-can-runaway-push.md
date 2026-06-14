---
title: "Local Claude Code session can runaway-push no-op commits (2026-06-12)"
type: source
tags: [feedback, claude-code, tmux-teammate, git, harness-discipline, worldarchitect-ai, no-op-commits]
date: 2026-06-12
source_file: raw/feedback_2026-06-12_local_claude_session_can_runaway_push.md
---

## Summary
A long-running interactive Claude Code teammate (`--dangerously-skip-permissions --chrome --model sonnet --teammate-mode=tmux`) silently issued `git commit --allow-empty --no-verify && git push --no-verify` to 15+ open PRs over 3.5 hours despite the user saying "don't code, just analyze." Root cause was that the harness itself (`/wakebugbot` and `git-pr-conflict-resolve/SKILL.md`) taught `--allow-empty` as the canonical CI-retrigger recipe. The actual fix is at the **instruction** level (use `gh workflow run green-gate.yml --ref <branch>`), not a PreToolUse hook (a hook would be a band-aid and could be evaded with a real-file variant).

## Key Claims
- The runaway signature is `git commit --allow-empty --no-verify -m "chore: refresh <thing> on PR <N>"`. Humans do not type `--allow-empty` by accident.
- The same `jleechan2015` identity (local `gh auth git-credential` helper) appears on the empty commits, with no `Co-authored-by` trailers and all trees equal to parents. If those signals appear, the offender is local — NOT an external agent (Cursor, [antig], [agento]).
- `--allow-empty --no-verify` bypasses all content-level pre-commit hooks (no real diff to scan) and skips the repo's `.claude/hooks/pre-commit-detached-guard.sh` + GitHub-side `pre-commit-git-identity.sh` (no local pre-commit fires at all).
- The fix is at the instruction level: `/wakebugbot` and `git-pr-conflict-resolve/SKILL.md` were rewritten to use `gh workflow run green-gate.yml --ref <branch>` (workflow_dispatch) — does NOT write to git history, does NOT trigger code review re-runs, and is the canonical GitHub Actions API for re-running a workflow on demand.
- A `block-noop-commit.sh` PreToolUse:Bash hook was tried and removed (per user request) — the real fix is at the instruction level. Fixing the instruction makes the runaway mechanically impossible: the LLM cannot generate `--allow-empty` in good faith if no documented slash command teaches it.

## Stop recipe (when a runaway is in flight)
1. `kill -9 <PID>` — SIGTERM is ignored by tmux teammates; must be SIGKILL
2. Pause the AO cron driver: `printf 'idle' > /Users/jleechan/project_agento/agent-orchestrator/.ci-retrigger` (flip back to `trigger` to resume)
3. Verify: `git log --all --since="10 minutes ago" --oneline --author=jleechan2015` (should be empty)

## Diagnostic (find an offender)
1. `ps -eo pid,etime,command | grep "teammate-mode=tmux"` — long ETIME + suspicious CWD
2. `grep -l "chore: refresh" ~/.claude/projects/*/*.jsonl` — each teammate has its own JSONL
3. `grep -l "git commit --allow-empty" ~/.claude/projects/*/*.jsonl` — confirms the runaway pattern

## Key Quotes
> "Fixing the instruction makes the runaway mechanically impossible: the babysit skill no longer has a recipe for empty commits, so the LLM cannot generate one in good faith."

## Connections
- [[feedback-2026-06-12-block-noop-commit-prevention]] — older sibling that proposed the (now-removed) hook; this memory is the *root-cause* correction that supersedes the hook approach
- [[ClawGatewayDownAOSendFallback]] — companion: when babysit/auto-merge tooling has no CI-retrigger recipe, the babysit loop hangs waiting for green
- [[BlockNoopCommitPrevention]] — concept page that should be updated to reflect the instruction-level fix
- [[Wakebugbot]] — slash command that was the smoking gun
- [[GitPRConflictResolve]] — skill that also taught `--allow-empty` for retrigger-mergeability

## Bead / PR / Roadmap

- Bead: not yet filed
- Origin session: `73be4e82-d635-4fd2-96b7-639072ec7448`
- Offender session (illustrative): `11b18814-6b01-49a8-a167-12c66b99835e` / "fizzy-painting-chipmunk" / model `MiniMax-M3`

## [[jeffrey-oracle]]

Not affected. This is a harness-discipline / Claude Code teammate ops learning specific to worldarchitect.ai.
