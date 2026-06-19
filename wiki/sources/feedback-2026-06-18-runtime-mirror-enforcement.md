---
title: "Runtime mirror enforcement: hook + skill doc + CLAUDE.md pointer"
type: source
tags: [feedback, self-hosted-oss, infra, github-actions, runners, pr-workflow, hooks]
date: 2026-06-18
source_file: ../../raw/feedback-2026-06-18-runtime-mirror-enforcement.md
---

## Summary
On 2026-06-18, PR #7666 (jleechanorg/worldarchitect.ai) merged a three-layer enforcement of the "edit self-hosted-oss/ in the repo, sync via install.sh" rule: (1) PreToolUse hook at `~/.claude/hooks/block-runtime-mirror-edits.sh` blocks direct Edit/Write on `~/.local/share/worldarchitect-runners/*.sh`; (2) skill doc at `.claude/skills/runtime-mirror-sync/SKILL.md`; (3) 3-line CLAUDE.md pointer. Same pattern applies to `~/.config/mcp-daemon/start-mcp-daemons.sh`, `~/Library/LaunchAgents/*.plist`, and `~/.hermes/`. The hook is the load-bearing layer; the others are discoverability.

## Key Claims
- `~/.local/share/worldarchitect-runners/` is a runtime mirror populated by `self-hosted-oss/install.sh`'s `RUNTIME_SCRIPTS` array from `self-hosted-oss/*.sh` in the worldarchitect.ai repo. Editing the mirror directly is the "I edited the wrong file" anti-pattern: the change is clobbered on the next `install.sh` run AND never propagates to other Macs.
- Three enforcement layers are needed: PreToolUse hook (load-bearing), skill doc (discoverability), CLAUDE.md pointer (discoverability). The hook alone is invisible; one learns "don't edit the mirror" but not why. The skill doc alone can be skipped if no one reads it. CLAUDE.md alone is too short to hold the full procedure.
- Other 5 CodeRabbit findings in PR #7666 addressed: `_cred_marker()` helper in wrapper (replaces leaky `${VAR:+<set>}${VAR:-<MISSING>}` pattern that actually substitutes the value), `RUNNER_INSTALL_DIR` override, captured `stop_err`/`rm_err` in heal-runners, install.sh renders plist from committed template, CLAUDE.md verbosity moved to skill doc.
- CR CHANGES_REQUESTED is the merge gate even when user's prior choice is the conflict — the user had explicitly kept the credential-leaking wrapper pattern as a debugging convenience; CR flagged as CRITICAL; fix preserves the set/unset signal via `${VAR:+<set>}${VAR:+<MISSING>}` (use `:+` for BOTH branches, not the asymmetric `${VAR:+<set>}${VAR:-<MISSING>}`).
- The fix is fleet-wide: hook is user-scope (applies to all jleechanorg repos that use the shared runner pool), skill doc + CLAUDE.md live in the worldarchitect.ai repo (the canonical home for these scripts), and the runtime mirror syncs via `bash self-hosted-oss/install.sh` on every host.

## Key Quotes
> "we need a PR are you stupid, all the setup needs to be in this repo and tracked in git, /learn and then do it" — user, 2026-06-18, after I was about to Edit `~/.local/share/worldarchitect-runners/heal-runners.sh` directly to test a quick fix

> "Containerized infra scripts that are 'the source of truth' must live in the repo, not on a host. The launchd/runtime mirror pattern is just one instance — same trap exists for `~/.config/mcp-daemon/start-mcp-daemons.sh` (mirrors MCP server definitions), `~/.hermes/` config (mirrors Hermes), `~/Library/LaunchAgents/*.plist` (renders from templates in repo). For every 'X is populated by Y from the repo' pattern: enforce with a hook + a skill doc + a CLAUDE.md pointer. All three. Not one of three."

> "When you encounter a new runtime-mirror pattern, write a hook that blocks direct edits, write a skill doc that explains the sync flow, add a CLAUDE.md pointer. All three. Not one of three."

## Connections
- [[heal-runners-sigkill-session-conflict-loop]] — companion memory covering the SIGKILL→session-conflict root cause in the same PR; the runtime-mirror enforcement is the other durable output.
- [[MCP-daemon-start-stdio-server-env-drop]] — same pattern in `~/.config/mcp-daemon/start-mcp-daemon/`: a runtime mirror populated by `start-mcp-daemons.sh` from MCP server definitions. The same three-layer enforcement should apply.
- [[Hermes-launchd-plist-template]] — concept page for the `~/Library/LaunchAgents/*.plist` template pattern; install.sh renders from the committed template (also part of PR #7666).
- [[PreToolUse-hooks-fail-closed-vs-loader-brick]] — the load-bearing layer is the hook; "fail-CLOSED on guarded file, fail-OPEN at the loader/dep boundary". This PR follows the same rule.
- [[jleechanorg/worldarchitect.ai PR #7666]] — entity page for the fix PR (merged 2026-06-18 at HEAD `4113f17b38`).
- [[bead rev-m12qj]] — closed learning bead referencing this episode.
- [[bead rev-dsny5]] — closed companion bead for the SIGKILL fix in the same PR.
- [[self-hosted-oss]] — concept page for the repository convention that makes runtime-mirror enforcement necessary.
- [[Docker container lifecycle]] — concept page where the SIGTERM vs SIGKILL trade-off (the other PR finding) is documented.
