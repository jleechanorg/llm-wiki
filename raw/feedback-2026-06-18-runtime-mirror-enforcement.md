---
name: runtime-mirror-enforcement
description: "Why ~/.local/share/worldarchitect-runners/ is a runtime mirror and how the PreToolUse hook + skill doc + CLAUDE.md pointer keep edits out of the wrong place. Enforced fleet-wide, not per-repo."
metadata:
  node_type: memory
  type: feedback
  bead: rev-m12qj
  originSessionId: cddd86d9-cb68-4482-b37b-9b08aeaf6d2c
---

# Runtime mirror enforcement (PR #7666, 2026-06-18)

Companion to [[heal-runners-sigkill-session-conflict-loop]] — that captures the SIGKILL→session-conflict root cause. This one captures the **process** rule: `~/.local/share/worldarchitect-runners/` is a runtime mirror, not the source. Editing the mirror is the "I edited the wrong file" anti-pattern. PR #7666 enforced this rule fleet-wide.

PR: [jleechanorg/worldarchitect.ai#7666](https://github.com/jleechanorg/worldarchitect.ai/pull/7666) (merged 2026-06-18, HEAD `4113f17b38`)

## The wrong-file anti-pattern

`launchd` runs scripts out of `~/.local/share/worldarchitect-runners/` on every Mac. That directory is populated by `self-hosted-oss/install.sh`'s `RUNTIME_SCRIPTS` array from `self-hosted-oss/*.sh` in the worldarchitect.ai repo. Two things go wrong if you edit the mirror directly:

1. **The change is clobbered** the next time someone runs `install.sh` (next machine setup, next install for a new feature, etc).
2. **The change never propagates** to other Macs in the pool. The 6 Mac runners + jeff-ubuntu all have their own mirror; editing one is editing one.

In the heal-runners session, I almost made this mistake — was about to Edit `~/.local/share/worldarchitect-runners/heal-runners.sh` directly to test a quick fix. User stopped me: "we need a PR are you stupid, all the setup needs to be in this repo and tracked in git."

## The fix — three layers, all committed

### Layer 1: PreToolUse hook (user-scope, fleet-wide)

`~/.claude/hooks/block-runtime-mirror-edits.sh` — registered in `~/.claude/settings.json` PreToolUse with matcher `Edit|Write|MultiEdit`. Blocks direct Edit/Write on `~/.local/share/worldarchitect-runners/*.sh`. Exits 0 (allows) for `.jsonl`/`.log`/`.bak`/`.swp` (state files) and for Bash `cp`/`rsync` to the mirror (the explicit sync shortcut).

Override token: `RUNTIME-MIRROR EDIT APPROVED` — intentionally awkward to type for a local-only experiment that will revert before next install.sh.

### Layer 2: Skill doc (repo-scope, this repo)

`.claude/skills/runtime-mirror-sync/SKILL.md` (61 lines) — full procedure, sync flow, why each step matters. Linked from `.codex/skills/runtime-mirror-sync/SKILL.md` via the standard `scripts/sync_codex_claude_skills.py` mirror.

### Layer 3: CLAUDE.md pointer (repo-scope, this repo)

A 3-line subsection in CLAUDE.md ("Runtime mirror is NOT the source — edit `self-hosted-oss/`, sync via `install.sh`") that points at the skill doc and mentions the hook. Keeps CLAUDE.md under the 200-line contract.

## Correct flow for self-hosted-oss changes

1. Edit `self-hosted-oss/<script>.sh` in the worktree.
2. Commit + push + open a PR (infra changes need a PR; host-only edits drift and don't propagate).
3. After commit, sync the local mirror via Bash:
   ```bash
   cp self-hosted-oss/<script>.sh ~/.local/share/worldarchitect-runners/<script>.sh
   ```
4. After PR merges, re-run `bash self-hosted-oss/install.sh` on every other Mac so `RUNTIME_SCRIPTS` re-populates the mirror from the merged source.

## End-to-end verification (this session)

- Hook self-test: Edit on `~/.local/share/worldarchitect-runners/heal-runners.sh` → exit 2 with diagnostic pointing at the correct path. Edit on `self-hosted-oss/heal-runners.sh` → exit 0. Edit on `.jsonl` in mirror → exit 0. Bash `cp` to mirror → exit 0.
- Skill doc committed and mirrored to `.codex/skills/`.
- CLAUDE.md now has the 3-line pointer (was 8 lines pre-fix).
- After PR merge, ran `cp self-hosted-oss/heal-runners.sh ~/.local/share/worldarchitect-runners/heal-runners.sh` (3 files). `diff -q` confirms parity. Live wrapper test: stdout.log shows `HERMES_SLACK_BOT_TOKEN=<set>` (no value leaked) — the new `_cred_marker()` fix is live.

## Why three layers?

- Hook alone is invisible — you hit it once, learn "don't edit the mirror", then forget why. Skill doc + CLAUDE.md make the *why* discoverable.
- Skill doc alone can be skipped if no one reads it. Hook makes the wrong action impossible (or explicitly overridden with a token).
- CLAUDE.md alone is too short to hold the full procedure. Skill doc carries the detail.

## Other 5 findings in PR #7666 (besides the SIGKILL fix)

| Finding | File | Fix |
|---------|------|-----|
| **CRITICAL** credential leak | `ubuntu-runner-health-wrapper.sh:64-66` | `_cred_marker()` helper — prints only `<set>`/`<MISSING>`, never the value |
| **CRITICAL** hardcoded path | `ubuntu-runner-health-wrapper.sh:70` | Honour `RUNNER_INSTALL_DIR` with standard path fallback |
| **MAJOR** silent stderr | `heal-runners.sh:210-211` | Capture `stop_err`/`rm_err`, log real error, only increment `recycled` on full success |
| **NITPICK** inline plist | `install.sh:281-307` | Render committed plist template via `@HOME@`/`@INSTALL_DIR@`/`@LOG_DIR@` substitution |
| **NITPICK** CLAUDE.md verbosity | `CLAUDE.md:230-237` | Move to `.claude/skills/runtime-mirror-sync/SKILL.md`, keep pointer in CLAUDE.md |

Plus: home-dir init moved before first `$HOME` reference (sparse bash_profile + set -u no longer interact badly); `getent` → `dscl` (macOS-native, getent is Linux-only).

## Rule to mirror

> Containerized infra scripts that are "the source of truth" must live in the repo, not on a host. The launchd/runtime mirror pattern is just one instance — same trap exists for `~/.config/mcp-daemon/start-mcp-daemons.sh` (mirrors MCP server definitions), `~/.hermes/` config (mirrors Hermes), `~/Library/LaunchAgents/*.plist` (renders from templates in repo). For every "X is populated by Y from the repo" pattern: enforce with a hook + a skill doc + a CLAUDE.md pointer. The hook is the load-bearing layer; the others are discoverability.

**How to apply:** When you encounter a new runtime-mirror pattern, write a hook that blocks direct edits, write a skill doc that explains the sync flow, add a CLAUDE.md pointer. All three. Not one of three.

## References

- [PR #7666](https://github.com/jleechanorg/worldarchitect.ai/pull/7666) — merged 2026-06-18, HEAD `4113f17b38` (Merge commit)
- Hook: `~/.claude/hooks/block-runtime-mirror-edits.sh`
- Skill: `.claude/skills/runtime-mirror-sync/SKILL.md` + `.codex/skills/runtime-mirror-sync` symlink
- Companion: `feedback_2026-06-18_heal_runners_sigkill_session_conflict.md` (the SIGKILL root cause)
- Prior: `feedback_2026-06-09_runner_supervisor_and_ops.md` (the original "stable install path sync" rule)
- User quote (2026-06-18): "we need a PR are you stupid, all the setup needs to be in this repo and tracked in git, /learn and then do it"
