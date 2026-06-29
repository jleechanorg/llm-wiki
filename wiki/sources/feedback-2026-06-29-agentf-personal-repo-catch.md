---
title: "Pre-push hook caught agent-f content in user_scope backup repo — refactored to dropbox-only"
type: source
tags: [agent-f, push-safety, backup, jleechanorg, dropbox, personal-vs-work, credential-leakage]
date: 2026-06-29
source_file: ../raw/feedback_2026-06-29_agentf_personal_repo_catch.md
---

## Summary
While expanding the user_scope backup (BACKUP_ITEMS in `scripts/backup-home.sh`) to cover ~/.hermes / ~/.agent-orchestrator / etc., one Tier-2 row referenced `~/.claude-agent-f/` — the alternate Claude profile used by `claudeaf()` / Agnt-F org work. The pre-push hook `block-agentf-push-to-jleechanorg.sh` correctly caught the commit string and blocked `git push`. Refactored to dropbox-only (empty git_rel, populated dropbox_rel) so the local backup runs on the next launchd tick without ever pushing agent-f content to `jleechanorg/*` git mirrors. User explicit: "i dont want agentf stuff in my personal repo, htis is a good catch".

## Key Claims
- The `jleechanorg/*` vs `Agnt-F/*` org separation is enforced by hook, not by convention — push-safety hooks catch config-drift bugs that no LLM-edit review would catch.
- Even a dropbox-only BACKUP_ITEMS row is not safe to commit + push to jleechanorg if the row's text contains agent-f strings (`.claude-agent-f`, `claude_agent_f`, etc.) — the hook inspects the commit content, not the runtime behavior.
- Refactoring cost to fix was 1 line edit + 1 commit (local-only); the hook caught it before the user even noticed.

## Key Quotes
> "i dont want agentf stuff in my personal repo, htis is a good catch /learn and dont backup the agentf" — user, 2026-06-29

> "When the hook blocks a push to jleechanorg/*: inspect the block message; if the agent-f content is incidental (one BACKUP_ITEMS row referencing a path under ~/.claude-agent-f/), refactor to dropbox-only." — reusable rule

## Connections
- [[MacCompressorOOMPressureSignal]] — earlier lesson: delete-by-substring-match is the wrong signal; here the parallel: a single-source-of-truth safety net (push hook) catches what convention can't.
- [IntegrateHardStopPattern](../sources/feedback-2026-06-19-integrate-hard-stop-uncommitted-state.md) — analog: hard-stops are features; treat the push-hook block the same way (don't bypass, refactor to fit).
- bd-40o — closed tracking bead for this lesson.
- Hook: `/Users/jleechan/.claude/hooks/block-agentf-push-to-jleechanorg.sh`
- Commit: `f22dc55f9` (local-only, intentionally not pushed to jleechanorg/user_scope)
- Adjacent credential issues (NOT fixed in this PR): `~/.hermes/hermes.json` Slack tokens not in hermes .gitignore; `~/.chatgpt_codex_auth_state.json` 3-month-stale chatgpt cookies; `~/.claude-code-router/config.json` live minimax API key.